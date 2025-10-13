"""Tests for story detector."""

import pytest
from prismq.idea.classification import StoryDetector


class TestStoryDetector:
    """Test story detection functionality."""
    
    def test_initialization_default_threshold(self):
        """Test detector initialization with default threshold."""
        detector = StoryDetector()
        assert detector.confidence_threshold == 0.3
    
    def test_initialization_custom_threshold(self):
        """Test detector initialization with custom threshold."""
        detector = StoryDetector(confidence_threshold=0.5)
        assert detector.confidence_threshold == 0.5
    
    def test_detect_high_confidence_story_title(self):
        """Test detection with high-confidence story keywords in title."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="My AITA Story - Am I the Villain?",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        assert is_story is True
        assert confidence >= 0.5
        assert len(indicators) > 0
        assert any('aita' in ind.lower() for ind in indicators)
    
    def test_detect_medium_confidence_story_title(self):
        """Test detection with medium-confidence story keywords in title."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="My Toxic Relationship Experience",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        assert is_story is True
        assert confidence >= 0.3
        assert len(indicators) > 0
    
    def test_detect_non_story_tutorial(self):
        """Test detection rejects tutorial videos."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="How to Make Amazing Videos - Tutorial",
            description="Learn to make great content",
            tags=['tutorial', 'howto'],
            subtitle_text=""
        )
        
        assert is_story is False
        assert confidence == 0.0
        assert any('non-story' in ind.lower() for ind in indicators)
    
    def test_detect_non_story_gameplay(self):
        """Test detection rejects gameplay videos."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="Epic Gameplay Highlights",
            description="Amazing game moments",
            tags=['gameplay'],
            subtitle_text=""
        )
        
        assert is_story is False
        assert confidence == 0.0
    
    def test_detect_with_story_description(self):
        """Test detection uses description keywords."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="My Experience",
            description="This is my true story about what happened to me last year",
            tags=[],
            subtitle_text=""
        )
        
        assert is_story is True
        assert len(indicators) >= 2
    
    def test_detect_with_story_tags(self):
        """Test detection uses tag keywords."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="My Experience with Something",  # Add a small boost from title
            description="",
            tags=['storytime', 'true story', 'personal story'],
            subtitle_text=""
        )
        
        # Should be classified as story due to multiple story tags + title keyword
        assert is_story is True
        assert confidence >= 0.3
        assert any('tag:' in ind for ind in indicators)
    
    def test_detect_with_subtitle_first_person(self):
        """Test detection uses first-person subtitle indicators."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="My Video",
            description="",
            tags=[],
            subtitle_text="I was walking down the street when I had the craziest experience"
        )
        
        # Should have some confidence boost from subtitles
        assert any('subtitle:' in ind for ind in indicators)
    
    def test_detect_from_metadata(self):
        """Test detection from metadata dictionary."""
        detector = StoryDetector()
        
        metadata = {
            'title': 'TIFU: I Made a Huge Mistake',
            'description': 'Here is my confession about what happened',
            'tags': ['reddit story'],
            'subtitle_text': 'So this happened yesterday'
        }
        
        is_story, confidence, indicators = detector.detect_from_metadata(metadata)
        
        assert is_story is True
        assert confidence > 0.5
        assert len(indicators) >= 3
    
    def test_detect_with_multiple_anti_patterns(self):
        """Test detection rejects content with multiple anti-patterns."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="Product Review",
            description="Unboxing tutorial and guide for new users",
            tags=[],
            subtitle_text=""
        )
        
        assert is_story is False
        assert confidence == 0.0
    
    def test_detect_confidence_threshold(self):
        """Test confidence threshold determines classification."""
        # High threshold
        detector_strict = StoryDetector(confidence_threshold=0.8)
        
        is_story, confidence, _ = detector_strict.detect(
            title="My crazy experience",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        # Should have low confidence, below strict threshold
        assert is_story is False
        assert confidence < 0.8
        
        # Low threshold
        detector_lenient = StoryDetector(confidence_threshold=0.1)
        
        is_story, confidence, _ = detector_lenient.detect(
            title="My crazy experience",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        # Should pass lenient threshold
        assert is_story is True
        assert confidence >= 0.1
    
    def test_detect_empty_inputs(self):
        """Test detection with empty inputs."""
        detector = StoryDetector()
        
        is_story, confidence, indicators = detector.detect(
            title="",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        assert is_story is False
        assert confidence == 0.0
        assert len(indicators) == 0
    
    def test_story_title_keywords_weights(self):
        """Test that different keyword weights affect confidence."""
        detector = StoryDetector()
        
        # High-weight keyword
        _, confidence_high, _ = detector.detect(
            title="My Story Time",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        # Low-weight keyword
        _, confidence_low, _ = detector.detect(
            title="My Experience",
            description="",
            tags=[],
            subtitle_text=""
        )
        
        # High-weight should have higher confidence
        assert confidence_high > confidence_low
    
    def test_confidence_capped_at_one(self):
        """Test that confidence is capped at 1.0."""
        detector = StoryDetector()
        
        # Many story indicators
        is_story, confidence, _ = detector.detect(
            title="My AITA Storytime Confession Revenge",
            description="This is my true story about what happened to me. Let me tell you this tale.",
            tags=['storytime', 'true story', 'personal story', 'aita'],
            subtitle_text="I was so shocked. I had no idea this happened."
        )
        
        assert is_story is True
        assert confidence <= 1.0
