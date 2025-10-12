"""Tests for YouTube channel plugin."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.sources.youtube_channel_plugin import YouTubeChannelPlugin
from src.config import Config


class TestYouTubeChannelPlugin:
    """Test YouTube channel plugin functionality."""
    
    def test_initialization(self, tmp_path):
        """Test plugin initialization."""
        config = Mock()
        
        # Mock yt-dlp check to return True
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            assert plugin.config == config
            assert plugin.get_source_name() == "youtube_channel"
    
    def test_initialization_without_ytdlp(self, tmp_path):
        """Test plugin initialization fails without yt-dlp."""
        config = Mock()
        
        # Mock yt-dlp check to return False
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=False):
            with pytest.raises(ValueError, match="yt-dlp is not installed"):
                YouTubeChannelPlugin(config)
    
    def test_normalize_channel_url_with_full_url(self, tmp_path):
        """Test channel URL normalization with full URL."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            url = "https://www.youtube.com/@channelname"
            assert plugin._normalize_channel_url(url) == url
    
    def test_normalize_channel_url_with_handle(self, tmp_path):
        """Test channel URL normalization with handle."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            result = plugin._normalize_channel_url("@channelname")
            assert result == "https://www.youtube.com/@channelname"
    
    def test_normalize_channel_url_with_channel_id(self, tmp_path):
        """Test channel URL normalization with channel ID."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            result = plugin._normalize_channel_url("UC1234567890")
            assert result == "https://www.youtube.com/channel/UC1234567890"
    
    def test_normalize_channel_url_with_plain_name(self, tmp_path):
        """Test channel URL normalization with plain name."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            result = plugin._normalize_channel_url("channelname")
            assert result == "https://www.youtube.com/@channelname"
    
    def test_parse_srt_to_text(self, tmp_path):
        """Test SRT subtitle parsing."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            srt_content = """1
00:00:00,000 --> 00:00:02,000
Hello world

2
00:00:02,000 --> 00:00:04,000
This is a test
"""
            
            result = plugin._parse_srt_to_text(srt_content)
            assert result == "Hello world This is a test"
    
    def test_format_duration_iso8601(self, tmp_path):
        """Test ISO 8601 duration formatting."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            # Test various durations
            assert plugin._format_duration_iso8601(0) == "PT0S"
            assert plugin._format_duration_iso8601(45) == "PT45S"
            assert plugin._format_duration_iso8601(60) == "PT1M0S"
            assert plugin._format_duration_iso8601(90) == "PT1M30S"
            assert plugin._format_duration_iso8601(180) == "PT3M0S"
    
    def test_scrape_without_channel_url(self, tmp_path):
        """Test scraping without channel URL."""
        config = Mock()
        config.youtube_channel_url = None
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            # Should return empty list when no channel URL
            result = plugin.scrape()
            assert result == []
    
    def test_extract_tags(self, tmp_path):
        """Test tag extraction from metadata."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            metadata = {
                'channel': 'Test Channel',
                'categories': ['Entertainment', 'Music'],
                'tags': ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6']
            }
            
            result = plugin._extract_tags(metadata)
            
            # Should include base tags, channel, categories, and up to 5 video tags
            assert 'youtube_shorts' in result
            assert 'channel_short' in result
            assert 'Test Channel' in result
            assert 'category_Entertainment' in result
            assert 'tag1' in result
    
    def test_metadata_to_idea_basic(self, tmp_path):
        """Test converting metadata to idea format."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            metadata = {
                'id': 'test_video_id',
                'title': 'Test Video',
                'description': 'Test description',
                'view_count': 10000,
                'like_count': 500,
                'comment_count': 50,
                'upload_date': '20240101',
                'channel_id': 'UC123',
                'channel': 'Test Channel',
                'duration': 60,
                'width': 1080,
                'height': 1920,
                'fps': 30,
                'tags': ['test', 'video'],
                'categories': ['Entertainment']
            }
            
            result = plugin._metadata_to_idea(metadata)
            
            assert result is not None
            assert result['source_id'] == 'test_video_id'
            assert result['title'] == 'Test Video'
            assert result['description'] == 'Test description'
            assert 'metrics' in result
            assert result['metrics']['statistics']['viewCount'] == '10000'
            assert result['metrics']['statistics']['likeCount'] == '500'
    
    def test_metadata_to_idea_with_engagement_calculation(self, tmp_path):
        """Test engagement rate calculation in metadata conversion."""
        config = Mock()
        
        with patch.object(YouTubeChannelPlugin, '_check_ytdlp', return_value=True):
            plugin = YouTubeChannelPlugin(config)
            
            metadata = {
                'id': 'test_video_id',
                'title': 'Test Video',
                'description': 'Test description',
                'view_count': 10000,
                'like_count': 500,
                'comment_count': 100,
                'upload_date': '20240101',
                'duration': 60,
                'width': 1080,
                'height': 1920,
                'tags': [],
                'categories': []
            }
            
            result = plugin._metadata_to_idea(metadata)
            
            # Engagement rate = (likes + comments) / views * 100
            expected_rate = (500 + 100) / 10000 * 100
            assert result['metrics']['enhanced_metrics']['engagement_rate'] == expected_rate


class TestYouTubeChannelPluginShortFiltering:
    """Test YouTube Shorts duration and format filtering."""
    
    def test_shorts_max_duration_constant(self):
        """Test that SHORTS_MAX_DURATION is set correctly."""
        assert YouTubeChannelPlugin.SHORTS_MAX_DURATION == 180
    
    def test_shorts_fetch_multiplier_constant(self):
        """Test that SHORTS_FETCH_MULTIPLIER is set correctly."""
        assert YouTubeChannelPlugin.SHORTS_FETCH_MULTIPLIER == 2
