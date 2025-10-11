"""Scoring engine for PrismQ.IdeaCollector."""

from typing import Dict, Any, List, Optional


class ScoringEngine:
    """Calculates scores for ideas based on various metrics."""

    def __init__(self, weights: Optional[List[float]] = None):
        """Initialize scoring engine.
        
        Args:
            weights: List of weights for scoring components
        """
        self.weights = weights or [1.0, 0.8, 0.6]

    def calculate_score(self, metrics: Dict[str, Any]) -> tuple:
        """Calculate overall score and score dictionary for an idea.
        
        Args:
            metrics: Dictionary of metrics (views, likes, comments, etc.)
            
        Returns:
            Tuple of (final_score, score_dictionary)
        """
        score_dict = {}
        
        # Extract common metrics
        views = metrics.get('views', 0)
        likes = metrics.get('likes', 0)
        comments = metrics.get('comments', 0)
        shares = metrics.get('shares', 0)
        
        # Calculate engagement rate
        if views > 0:
            engagement_rate = (likes + comments + shares) / views
        else:
            engagement_rate = 0
        
        # Calculate individual scores
        score_dict['view_score'] = self._normalize_metric(views, 1000000)
        score_dict['like_score'] = self._normalize_metric(likes, 50000)
        score_dict['comment_score'] = self._normalize_metric(comments, 1000)
        score_dict['engagement_score'] = min(engagement_rate * 100, 1.0)
        
        # Apply weights and calculate final score
        components = [
            score_dict['view_score'],
            score_dict['like_score'],
            score_dict['comment_score'],
            score_dict['engagement_score']
        ]
        
        # Pad or trim components to match weights
        while len(components) < len(self.weights):
            components.append(0.0)
        components = components[:len(self.weights)]
        
        # Calculate weighted sum
        final_score = sum(comp * weight for comp, weight in zip(components, self.weights))
        
        # Normalize to 0-100 scale
        final_score = min(final_score * 10, 100.0)
        
        score_dict['final_score'] = final_score
        
        return final_score, score_dict

    @staticmethod
    def _normalize_metric(value: float, max_value: float) -> float:
        """Normalize a metric to 0-1 scale.
        
        Args:
            value: Raw metric value
            max_value: Maximum expected value for normalization
            
        Returns:
            Normalized value between 0 and 1
        """
        if max_value <= 0:
            return 0.0
        return min(value / max_value, 1.0)

    def calculate_reddit_score(self, post_data: Dict[str, Any]) -> tuple:
        """Calculate score for a Reddit post.
        
        Args:
            post_data: Reddit post data
            
        Returns:
            Tuple of (final_score, score_dictionary)
        """
        metrics = {
            'views': post_data.get('num_views', 0) or 0,
            'likes': post_data.get('score', 0) or post_data.get('ups', 0),
            'comments': post_data.get('num_comments', 0),
            'shares': 0  # Reddit doesn't provide share count
        }
        return self.calculate_score(metrics)

    def calculate_youtube_score(self, video_data: Dict[str, Any]) -> tuple:
        """Calculate score for a YouTube video.
        
        Args:
            video_data: YouTube video statistics
            
        Returns:
            Tuple of (final_score, score_dictionary)
        """
        stats = video_data.get('statistics', {})
        metrics = {
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'shares': 0  # YouTube API doesn't provide direct share count
        }
        return self.calculate_score(metrics)
