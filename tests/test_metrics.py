"""Tests for universal metrics module."""

import pytest
from src.metrics import UniversalMetrics


def test_universal_metrics_initialization():
    """Test basic metrics initialization."""
    metrics = UniversalMetrics(
        platform="youtube",
        view_count=10000,
        like_count=500,
        comment_count=50,
        share_count=25
    )
    
    assert metrics.platform == "youtube"
    assert metrics.view_count == 10000
    assert metrics.like_count == 500
    assert metrics.comment_count == 50
    assert metrics.share_count == 25


def test_calculate_derived_metrics():
    """Test derived metrics calculation."""
    metrics = UniversalMetrics(
        view_count=10000,
        like_count=500,
        comment_count=50,
        share_count=25
    )
    
    metrics.calculate_derived_metrics()
    
    # Engagement rate = (500 + 50 + 25) / 10000 * 100 = 5.75%
    assert metrics.engagement_rate == pytest.approx(5.75, rel=0.01)
    
    # Like to view ratio = 500 / 10000 * 100 = 5%
    assert metrics.like_to_view_ratio == pytest.approx(5.0, rel=0.01)
    
    # Comment to view ratio = 50 / 10000 * 100 = 0.5%
    assert metrics.comment_to_view_ratio == pytest.approx(0.5, rel=0.01)
    
    # Share to view ratio = 25 / 10000 * 100 = 0.25%
    assert metrics.share_to_view_ratio == pytest.approx(0.25, rel=0.01)


def test_from_youtube():
    """Test creating metrics from YouTube data."""
    youtube_data = {
        'id': 'test_video_id',
        'snippet': {
            'title': 'Test Video Title',
            'description': 'Test description',
            'publishedAt': '2024-01-01T00:00:00Z',
            'channelId': 'test_channel',
            'channelTitle': 'Test Channel',
            'categoryId': '22',
            'tags': ['tag1', 'tag2', 'tag3']
        },
        'statistics': {
            'viewCount': '10000',
            'likeCount': '500',
            'commentCount': '50',
            'favoriteCount': '10'
        },
        'contentDetails': {
            'duration': 'PT45S'
        }
    }
    
    metrics = UniversalMetrics.from_youtube(youtube_data)
    
    assert metrics.platform == "youtube"
    assert metrics.view_count == 10000
    assert metrics.like_count == 500
    assert metrics.comment_count == 50
    assert metrics.favorite_count == 10
    assert metrics.title_length == len('Test Video Title')
    assert metrics.description_length == len('Test description')
    assert metrics.tag_count == 3
    assert metrics.engagement_rate is not None


def test_from_reddit():
    """Test creating metrics from Reddit data."""
    reddit_data = {
        'score': 1000,
        'ups': 1050,
        'num_comments': 150,
        'upvote_ratio': 0.95,
        'title': 'Test Reddit Post',
        'selftext': 'This is a test post with some content',
        'num_views': 5000
    }
    
    metrics = UniversalMetrics.from_reddit(reddit_data)
    
    assert metrics.platform == "reddit"
    assert metrics.like_count == 1000  # Reddit score
    assert metrics.upvote_count == 1050
    assert metrics.comment_count == 150
    assert metrics.upvote_ratio == 0.95
    assert metrics.title_length == len('Test Reddit Post')
    assert metrics.description_length == len('This is a test post with some content')


def test_to_dict_excludes_none():
    """Test that to_dict excludes None values."""
    metrics = UniversalMetrics(
        platform="youtube",
        view_count=10000,
        like_count=500
    )
    
    metrics_dict = metrics.to_dict()
    
    # Should include set values
    assert 'platform' in metrics_dict
    assert 'view_count' in metrics_dict
    assert 'like_count' in metrics_dict
    
    # Should exclude None values
    assert 'dislike_count' not in metrics_dict
    assert 'upvote_count' not in metrics_dict


def test_views_per_day_calculation():
    """Test views per day calculation."""
    metrics = UniversalMetrics(
        view_count=10000,
        days_since_upload=10
    )
    
    metrics.calculate_derived_metrics()
    
    # Views per day = 10000 / 10 = 1000
    assert metrics.views_per_day == 1000.0
    
    # Views per hour = 1000 / 24 = 41.67
    assert metrics.views_per_hour == pytest.approx(41.67, rel=0.01)


def test_zero_views_no_error():
    """Test that zero views doesn't cause division errors."""
    metrics = UniversalMetrics(
        view_count=0,
        like_count=10,
        comment_count=5
    )
    
    # Should not raise an error
    metrics.calculate_derived_metrics()
    
    # Ratios should be None when views are 0
    assert metrics.engagement_rate is None
    assert metrics.like_to_view_ratio is None
