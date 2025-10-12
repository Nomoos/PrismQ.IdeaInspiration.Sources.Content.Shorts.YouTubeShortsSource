"""Tests for scoring engine."""

import pytest
from src.scoring import ScoringEngine


def test_scoring_engine_initialization():
    """Test scoring engine initialization."""
    engine = ScoringEngine()
    assert engine.weights == [1.0, 0.8, 0.6]
    
    custom_engine = ScoringEngine([2.0, 1.5, 1.0])
    assert custom_engine.weights == [2.0, 1.5, 1.0]


def test_calculate_score_basic():
    """Test basic score calculation."""
    engine = ScoringEngine()
    metrics = {
        'views': 10000,
        'likes': 500,
        'comments': 50,
        'shares': 10
    }
    
    score, score_dict = engine.calculate_score(metrics)
    
    assert isinstance(score, float)
    assert score > 0
    assert 'final_score' in score_dict
    assert 'view_score' in score_dict
    assert 'like_score' in score_dict


def test_calculate_score_zero_views():
    """Test score calculation with zero views."""
    engine = ScoringEngine()
    metrics = {
        'views': 0,
        'likes': 0,
        'comments': 0,
        'shares': 0
    }
    
    score, score_dict = engine.calculate_score(metrics)
    
    assert score >= 0
    assert score_dict['engagement_score'] == 0


def test_normalize_metric():
    """Test metric normalization."""
    # Test normal case
    result = ScoringEngine._normalize_metric(500, 1000)
    assert result == 0.5
    
    # Test exceeding max
    result = ScoringEngine._normalize_metric(1500, 1000)
    assert result == 1.0
    
    # Test zero max
    result = ScoringEngine._normalize_metric(100, 0)
    assert result == 0.0


def test_calculate_reddit_score():
    """Test Reddit-specific score calculation."""
    engine = ScoringEngine()
    post_data = {
        'score': 1000,
        'ups': 1000,
        'num_comments': 50,
        'upvote_ratio': 0.95
    }
    
    score, score_dict = engine.calculate_reddit_score(post_data)
    
    assert isinstance(score, float)
    assert score > 0


def test_calculate_youtube_score():
    """Test YouTube-specific score calculation."""
    engine = ScoringEngine()
    video_data = {
        'statistics': {
            'viewCount': '100000',
            'likeCount': '5000',
            'commentCount': '200'
        }
    }
    
    score, score_dict = engine.calculate_youtube_score(video_data)
    
    assert isinstance(score, float)
    assert score > 0


def test_different_weights_affect_score():
    """Test that different weights produce different scores."""
    metrics = {
        'views': 10000,
        'likes': 500,
        'comments': 50,
        'shares': 10
    }
    
    engine1 = ScoringEngine([1.0, 1.0, 1.0])
    score1, _ = engine1.calculate_score(metrics)
    
    engine2 = ScoringEngine([2.0, 1.0, 0.5])
    score2, _ = engine2.calculate_score(metrics)
    
    # Scores should be different with different weights
    assert score1 != score2


def test_calculate_engagement_rate():
    """Test Engagement Rate (ER) calculation."""
    engine = ScoringEngine()
    
    # Test with all engagement metrics
    metrics = {
        'views': 10000,
        'likes': 500,
        'comments': 50,
        'shares': 30,
        'saves': 20
    }
    
    er = engine.calculate_engagement_rate(metrics)
    # ER = (500 + 50 + 30 + 20) / 10000 * 100 = 6.0%
    assert er == 6.0
    
    # Test with zero views
    metrics_no_views = {
        'views': 0,
        'likes': 100,
        'comments': 10,
        'shares': 5,
        'saves': 5
    }
    er_zero = engine.calculate_engagement_rate(metrics_no_views)
    assert er_zero == 0.0


def test_calculate_watch_through_rate():
    """Test Watch-Through/Completion Rate calculation."""
    engine = ScoringEngine()
    
    # Test normal case
    metrics = {
        'average_watch_time': 45,  # 45 seconds
        'video_length': 60  # 60 seconds
    }
    wtr = engine.calculate_watch_through_rate(metrics)
    # WTR = 45 / 60 * 100 = 75%
    assert wtr == 75.0
    
    # Test exceeding 100%
    metrics_exceed = {
        'average_watch_time': 120,
        'video_length': 60
    }
    wtr_exceed = engine.calculate_watch_through_rate(metrics_exceed)
    assert wtr_exceed == 100.0
    
    # Test zero length
    metrics_zero = {
        'average_watch_time': 30,
        'video_length': 0
    }
    wtr_zero = engine.calculate_watch_through_rate(metrics_zero)
    assert wtr_zero == 0.0


def test_calculate_conversion_rate():
    """Test Conversion Rate (CR) calculation."""
    engine = ScoringEngine()
    
    # Test normal case
    metrics = {
        'views': 10000,
        'conversions': 250  # subscribers, follows, clicks, etc.
    }
    cr = engine.calculate_conversion_rate(metrics)
    # CR = 250 / 10000 * 100 = 2.5%
    assert cr == 2.5
    
    # Test zero views
    metrics_zero = {
        'views': 0,
        'conversions': 10
    }
    cr_zero = engine.calculate_conversion_rate(metrics_zero)
    assert cr_zero == 0.0


def test_calculate_relative_performance_index():
    """Test Relative Performance Index (RPI) calculation."""
    engine = ScoringEngine()
    
    # Test performing at 200% of median
    metrics = {
        'views': 20000,
        'channel_median_views': 10000
    }
    rpi = engine.calculate_relative_performance_index(metrics, 'views')
    # RPI = 20000 / 10000 * 100 = 200%
    assert rpi == 200.0
    
    # Test performing at 50% of median
    metrics_below = {
        'views': 5000,
        'channel_median_views': 10000
    }
    rpi_below = engine.calculate_relative_performance_index(metrics_below, 'views')
    assert rpi_below == 50.0
    
    # Test with zero median
    metrics_zero = {
        'views': 10000,
        'channel_median_views': 0
    }
    rpi_zero = engine.calculate_relative_performance_index(metrics_zero, 'views')
    assert rpi_zero == 0.0
    
    # Test with different metric
    metrics_likes = {
        'likes': 500,
        'channel_median_likes': 250
    }
    rpi_likes = engine.calculate_relative_performance_index(metrics_likes, 'likes')
    assert rpi_likes == 200.0


def test_calculate_universal_content_score():
    """Test Universal Content Score (UCS) calculation."""
    engine = ScoringEngine()
    
    # Test comprehensive UCS calculation
    metrics = {
        'views': 20000,
        'likes': 1000,
        'comments': 100,
        'shares': 50,
        'saves': 50,
        'average_watch_time': 45,
        'video_length': 60,
        'channel_median_views': 10000,
        'conversions': 200
    }
    
    scores = engine.calculate_universal_content_score(metrics)
    
    # Verify all components are calculated
    assert 'universal_content_score' in scores
    assert 'engagement_rate' in scores
    assert 'watch_through_rate' in scores
    assert 'relative_performance_index' in scores
    assert 'conversion_rate' in scores
    
    # Verify engagement rate
    # ER = (1000 + 100 + 50 + 50) / 20000 * 100 = 6.0%
    assert scores['engagement_rate'] == 6.0
    
    # Verify watch-through rate
    # WTR = 45 / 60 * 100 = 75%
    assert scores['watch_through_rate'] == 75.0
    
    # Verify RPI
    # RPI = 20000 / 10000 * 100 = 200%
    assert scores['relative_performance_index'] == 200.0
    
    # Verify conversion rate
    # CR = 200 / 20000 * 100 = 1.0%
    assert scores['conversion_rate'] == 1.0
    
    # Verify UCS
    # UCS = 0.4 * 6.0 + 0.4 * 75.0 + 0.2 * (min(200, 200) / 2)
    # UCS = 2.4 + 30.0 + 20.0 = 52.4
    expected_ucs = 0.4 * 6.0 + 0.4 * 75.0 + 0.2 * (200.0 / 2.0)
    assert scores['universal_content_score'] == expected_ucs
    
    # Verify UCS is capped at 100
    assert scores['universal_content_score'] <= 100.0


def test_universal_content_score_with_minimal_data():
    """Test UCS with minimal/missing data."""
    engine = ScoringEngine()
    
    # Test with minimal metrics
    metrics = {
        'views': 1000,
        'likes': 50
    }
    
    scores = engine.calculate_universal_content_score(metrics)
    
    # Should not crash and should return valid structure
    assert 'universal_content_score' in scores
    assert scores['universal_content_score'] >= 0.0
    assert scores['universal_content_score'] <= 100.0


def test_engagement_rate_with_saves():
    """Test that saves are included in engagement rate calculation."""
    engine = ScoringEngine()
    
    metrics_with_saves = {
        'views': 10000,
        'likes': 20,
        'comments': 5,
        'shares': 3,
        'saves': 12
    }
    
    metrics_without_saves = {
        'views': 10000,
        'likes': 20,
        'comments': 5,
        'shares': 3,
        'saves': 0
    }
    
    # Calculate scores using the main calculate_score method
    _, score_dict_with = engine.calculate_score(metrics_with_saves)
    _, score_dict_without = engine.calculate_score(metrics_without_saves)
    
    # Engagement score should be different (with saves = 0.4%, without = 0.28%)
    assert score_dict_with['engagement_score'] > score_dict_without['engagement_score']
    
    # Also test with calculate_engagement_rate method
    er_with = engine.calculate_engagement_rate(metrics_with_saves)
    er_without = engine.calculate_engagement_rate(metrics_without_saves)
    
    # (20+5+3+12)/10000 * 100 = 0.4%
    assert abs(er_with - 0.4) < 0.001
    # (20+5+3+0)/10000 * 100 = 0.28%
    assert abs(er_without - 0.28) < 0.001
    
    # Verify saves make a difference
    assert er_with > er_without

