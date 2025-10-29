"""Tests for the IdeaProcessor module."""

import pytest
import json
from datetime import datetime, timezone
from processor.idea_processor import IdeaProcessor, IdeaInspiration, ContentType


class MockYouTubeShortsRecord:
    """Mock YouTubeShortsSource record for testing."""
    
    def __init__(
        self,
        id=1,
        source="youtube",
        source_id="test_video_123",
        title="Test Video Title",
        description="Test video description",
        tags="tag1, tag2, tag3",
        score=85.5,
        score_dictionary=None,
        processed=False,
        created_at=None,
        updated_at=None
    ):
        self.id = id
        self.source = source
        self.source_id = source_id
        self.title = title
        self.description = description
        self.tags = tags
        self.score = score
        self._score_dictionary = score_dictionary
        self.processed = processed
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
    
    def get_score_dict(self):
        """Get score dictionary as Python dict."""
        if self._score_dictionary:
            if isinstance(self._score_dictionary, str):
                return json.loads(self._score_dictionary)
            return self._score_dictionary
        return None


class TestIdeaProcessorBasic:
    """Test basic IdeaProcessor functionality."""
    
    def test_process_minimal_record(self):
        """Test processing record with minimal required fields."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            description=None,
            tags=None,
            score=None,
            score_dictionary=None
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.title == "Test Title"
        assert idea.source_id == "abc123"
        assert idea.description == ""
        assert idea.content == ""
        assert idea.keywords == []
        assert idea.source_type == ContentType.VIDEO
        assert idea.source_url == "https://www.youtube.com/shorts/abc123"
        assert idea.score is None
    
    def test_process_with_description(self):
        """Test processing record with description."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            description="This is a test description"
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.description == "This is a test description"
    
    def test_process_with_tags(self):
        """Test processing record with tags."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            tags="python, programming, tutorial"
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.keywords == ["python", "programming", "tutorial"]
    
    def test_process_with_empty_tags(self):
        """Test processing record with empty tags."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            tags=""
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.keywords == []
    
    def test_process_with_score(self):
        """Test processing record with score."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score=85.7
        )
        
        idea = IdeaProcessor.process(record)
        
        # Score should be rounded to nearest integer
        assert idea.score == 86


class TestIdeaProcessorWithMetadata:
    """Test IdeaProcessor with score_dictionary metadata."""
    
    def test_process_with_subtitle_text(self):
        """Test processing record with subtitle text in enhanced_metrics."""
        score_dict = {
            'enhanced_metrics': {
                'subtitle_text': 'This is the subtitle text from the video',
                'subtitles_available': True
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.content == 'This is the subtitle text from the video'
        assert idea.metadata['subtitles_available'] == 'True'
    
    def test_process_with_statistics(self):
        """Test processing record with statistics."""
        score_dict = {
            'statistics': {
                'viewCount': '100000',
                'likeCount': '5000',
                'commentCount': '500'
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.metadata['views'] == '100000'
        assert idea.metadata['likes'] == '5000'
        assert idea.metadata['comments'] == '500'
        assert idea.metadata['platform'] == 'youtube_shorts'
    
    def test_process_with_enhanced_metrics(self):
        """Test processing record with enhanced metrics."""
        score_dict = {
            'enhanced_metrics': {
                'engagement_rate': 5.5,
                'views_per_day': 1000.5,
                'resolution': '1080x1920',
                'fps': 30,
                'aspect_ratio': '9:16',
                'channel_follower_count': 50000
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.metadata['engagement_rate'] == '5.5'
        assert idea.metadata['views_per_day'] == '1000.5'
        assert idea.metadata['resolution'] == '1080x1920'
        assert idea.metadata['fps'] == '30'
        assert idea.metadata['aspect_ratio'] == '9:16'
        assert idea.metadata['channel_follower_count'] == '50000'
    
    def test_process_with_snippet_data(self):
        """Test processing record with snippet data."""
        score_dict = {
            'snippet': {
                'channelId': 'UC123456',
                'channelTitle': 'Test Channel',
                'publishedAt': '20241015',
                'categoryId': '22'
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.metadata['channel_id'] == 'UC123456'
        assert idea.metadata['channel_title'] == 'Test Channel'
        assert idea.metadata['published_at'] == '20241015'
        assert idea.metadata['category_id'] == '22'
        assert idea.source_created_by == 'Test Channel'
    
    def test_process_with_content_details(self):
        """Test processing record with content details."""
        score_dict = {
            'contentDetails': {
                'duration': 'PT45S'
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        assert idea.metadata['duration'] == 'PT45S'


class TestIdeaProcessorComprehensive:
    """Test IdeaProcessor with comprehensive data."""
    
    def test_process_full_record(self):
        """Test processing record with all fields populated."""
        score_dict = {
            'snippet': {
                'title': 'Full Test Video',
                'description': 'Complete description',
                'publishedAt': '2024-10-15T10:30:00Z',
                'channelId': 'UC123456',
                'channelTitle': 'Tech Channel',
                'categoryId': '22',
                'tags': ['tech', 'tutorial']
            },
            'statistics': {
                'viewCount': '250000',
                'likeCount': '12500',
                'commentCount': '1250',
                'favoriteCount': '0'
            },
            'contentDetails': {
                'duration': 'PT1M30S'
            },
            'enhanced_metrics': {
                'engagement_rate': 5.5,
                'views_per_day': 5000.0,
                'resolution': '1080x1920',
                'fps': 60,
                'aspect_ratio': '9:16',
                'subtitle_text': 'Welcome to this tutorial on Python programming',
                'subtitles_available': True,
                'channel_follower_count': 100000
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Full Test Video",
            source_id="xyz789",
            description="Complete description",
            tags="python, programming, tutorial, tech",
            score=92.3,
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        # Basic fields
        assert idea.title == "Full Test Video"
        assert idea.description == "Complete description"
        assert idea.source_id == "xyz789"
        assert idea.source_type == ContentType.VIDEO
        assert idea.source_url == "https://www.youtube.com/shorts/xyz789"
        assert idea.score == 92
        
        # Keywords
        assert idea.keywords == ["python", "programming", "tutorial", "tech"]
        
        # Content (subtitles)
        assert idea.content == 'Welcome to this tutorial on Python programming'
        
        # Source info
        assert idea.source_created_by == 'Tech Channel'
        assert idea.source_created_at == '2024-10-15T10:30:00Z'
        
        # Metadata - statistics
        assert idea.metadata['views'] == '250000'
        assert idea.metadata['likes'] == '12500'
        assert idea.metadata['comments'] == '1250'
        
        # Metadata - enhanced
        assert idea.metadata['engagement_rate'] == '5.5'
        assert idea.metadata['views_per_day'] == '5000.0'
        assert idea.metadata['resolution'] == '1080x1920'
        assert idea.metadata['fps'] == '60'
        assert idea.metadata['aspect_ratio'] == '9:16'
        assert idea.metadata['subtitles_available'] == 'True'
        assert idea.metadata['channel_follower_count'] == '100000'
        
        # Metadata - snippet
        assert idea.metadata['channel_id'] == 'UC123456'
        assert idea.metadata['channel_title'] == 'Tech Channel'
        assert idea.metadata['category_id'] == '22'
        
        # Metadata - platform
        assert idea.metadata['platform'] == 'youtube_shorts'
        assert idea.metadata['source_type'] == 'video'
    
    def test_to_dict_conversion(self):
        """Test that IdeaInspiration can be converted to dict."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            tags="tag1, tag2"
        )
        
        idea = IdeaProcessor.process(record)
        idea_dict = idea.to_dict()
        
        assert isinstance(idea_dict, dict)
        assert idea_dict['title'] == "Test Title"
        assert idea_dict['source_id'] == "abc123"
        assert idea_dict['source_type'] == ContentType.VIDEO
        assert idea_dict['keywords'] == ["tag1", "tag2"]
        assert 'metadata' in idea_dict


class TestIdeaProcessorEdgeCases:
    """Test IdeaProcessor edge cases and error handling."""
    
    def test_process_none_record(self):
        """Test processing None record raises ValueError."""
        with pytest.raises(ValueError, match="Record cannot be None"):
            IdeaProcessor.process(None)
    
    def test_process_record_without_title(self):
        """Test processing record without title raises ValueError."""
        record = MockYouTubeShortsRecord(
            title="",
            source_id="abc123"
        )
        
        with pytest.raises(ValueError, match="Record must have a title"):
            IdeaProcessor.process(record)
    
    def test_process_record_without_source_id(self):
        """Test processing record without source_id raises ValueError."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id=""
        )
        
        with pytest.raises(ValueError, match="Record must have a source_id"):
            IdeaProcessor.process(record)
    
    def test_process_with_none_score_dictionary(self):
        """Test processing record with None score_dictionary."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=None
        )
        
        idea = IdeaProcessor.process(record)
        
        # Should succeed with empty metadata
        assert idea.content == ""
        assert idea.metadata['platform'] == 'youtube_shorts'
    
    def test_process_with_empty_score_dictionary(self):
        """Test processing record with empty score_dictionary."""
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps({})
        )
        
        idea = IdeaProcessor.process(record)
        
        # Should succeed with minimal metadata
        assert idea.content == ""
        assert idea.metadata['platform'] == 'youtube_shorts'
    
    def test_extract_upload_date_yyyymmdd_format(self):
        """Test extracting upload date in YYYYMMDD format."""
        score_dict = {
            'snippet': {
                'publishedAt': '20241015'
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        # Should be converted to ISO 8601
        assert idea.source_created_at.startswith('2024-10-15')
    
    def test_extract_upload_date_iso8601_format(self):
        """Test extracting upload date in ISO 8601 format."""
        score_dict = {
            'snippet': {
                'publishedAt': '2024-10-15T10:30:00Z'
            }
        }
        
        record = MockYouTubeShortsRecord(
            title="Test Title",
            source_id="abc123",
            score_dictionary=json.dumps(score_dict)
        )
        
        idea = IdeaProcessor.process(record)
        
        # Should be preserved as-is
        assert idea.source_created_at == '2024-10-15T10:30:00Z'


class TestIdeaProcessorBatch:
    """Test batch processing functionality."""
    
    def test_process_batch_empty_list(self):
        """Test processing empty batch."""
        results = IdeaProcessor.process_batch([])
        
        assert results == []
    
    def test_process_batch_single_record(self):
        """Test processing batch with single record."""
        records = [
            MockYouTubeShortsRecord(
                title="Test 1",
                source_id="abc123"
            )
        ]
        
        results = IdeaProcessor.process_batch(records)
        
        assert len(results) == 1
        assert results[0].title == "Test 1"
    
    def test_process_batch_multiple_records(self):
        """Test processing batch with multiple records."""
        records = [
            MockYouTubeShortsRecord(
                title="Test 1",
                source_id="abc123"
            ),
            MockYouTubeShortsRecord(
                title="Test 2",
                source_id="def456"
            ),
            MockYouTubeShortsRecord(
                title="Test 3",
                source_id="ghi789"
            )
        ]
        
        results = IdeaProcessor.process_batch(records)
        
        assert len(results) == 3
        assert results[0].title == "Test 1"
        assert results[1].title == "Test 2"
        assert results[2].title == "Test 3"
    
    def test_process_batch_with_invalid_record(self):
        """Test that batch processing continues after encountering invalid record."""
        records = [
            MockYouTubeShortsRecord(
                title="Test 1",
                source_id="abc123"
            ),
            MockYouTubeShortsRecord(
                title="",  # Invalid - no title
                source_id="def456"
            ),
            MockYouTubeShortsRecord(
                title="Test 3",
                source_id="ghi789"
            )
        ]
        
        results = IdeaProcessor.process_batch(records)
        
        # Should process valid records and skip invalid one
        assert len(results) == 2
        assert results[0].title == "Test 1"
        assert results[1].title == "Test 3"


class TestSourceUrlBuilder:
    """Test source URL building."""
    
    def test_build_source_url(self):
        """Test building YouTube Shorts URL."""
        url = IdeaProcessor._build_source_url("abc123")
        assert url == "https://www.youtube.com/shorts/abc123"
    
    def test_build_source_url_with_special_chars(self):
        """Test building URL with special characters in video ID."""
        url = IdeaProcessor._build_source_url("abc-123_xyz")
        assert url == "https://www.youtube.com/shorts/abc-123_xyz"
