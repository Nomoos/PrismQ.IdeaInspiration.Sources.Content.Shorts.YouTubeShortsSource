"""Tests for YouTube plugin."""

import pytest
from src.sources.youtube_plugin import YouTubePlugin


class TestYouTubePluginShortDuration:
    """Test YouTube Shorts duration validation."""
    
    def test_is_short_with_short_video(self):
        """Test that videos under 180 seconds are identified as Shorts."""
        # 45 seconds
        assert YouTubePlugin._is_short('PT45S') == True
        
        # 1 minute
        assert YouTubePlugin._is_short('PT1M') == True
        
        # 1 minute 30 seconds (90 seconds)
        assert YouTubePlugin._is_short('PT1M30S') == True
        
        # 2 minutes 59 seconds (179 seconds)
        assert YouTubePlugin._is_short('PT2M59S') == True
        
        # Exactly 3 minutes (180 seconds) - should be included
        assert YouTubePlugin._is_short('PT3M') == True
        assert YouTubePlugin._is_short('PT2M60S') == True  # Alternative format
    
    def test_is_short_with_long_video(self):
        """Test that videos over 180 seconds are not identified as Shorts."""
        # 3 minutes 1 second (181 seconds)
        assert YouTubePlugin._is_short('PT3M1S') == False
        
        # 4 minutes
        assert YouTubePlugin._is_short('PT4M') == False
        
        # 5 minutes 30 seconds
        assert YouTubePlugin._is_short('PT5M30S') == False
        
        # 10 minutes
        assert YouTubePlugin._is_short('PT10M') == False
    
    def test_is_short_with_edge_cases(self):
        """Test edge cases for Shorts duration."""
        # 0 seconds
        assert YouTubePlugin._is_short('PT0S') == True
        
        # Just seconds under limit (180 seconds)
        assert YouTubePlugin._is_short('PT180S') == True
        
        # Just over limit
        assert YouTubePlugin._is_short('PT181S') == False
        
        # Invalid format
        assert YouTubePlugin._is_short('INVALID') == False
        assert YouTubePlugin._is_short('') == False
    
    def test_is_short_boundary_values(self):
        """Test boundary values around 180 second limit."""
        # Values right at the boundary
        assert YouTubePlugin._is_short('PT2M59S') == True  # 179 seconds
        assert YouTubePlugin._is_short('PT3M0S') == True   # 180 seconds
        assert YouTubePlugin._is_short('PT3M1S') == False  # 181 seconds
