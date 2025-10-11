"""Tests for scoring engine."""

import pytest
from idea_collector.scoring import ScoringEngine


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
