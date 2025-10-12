"""Scoring engine for PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource."""

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
        saves = metrics.get('saves', 0)
        
        # Calculate engagement rate (includes saves for universal metric compatibility)
        if views > 0:
            engagement_rate = (likes + comments + shares + saves) / views
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

    def calculate_engagement_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate Engagement Rate (ER).
        
        Formula: ER = (likes + comments + shares + saves) / views × 100%
        
        Args:
            metrics: Dictionary containing views, likes, comments, shares, saves
            
        Returns:
            Engagement rate as a percentage (0-100)
        """
        views = metrics.get('views', 0)
        if views == 0:
            return 0.0
        
        likes = metrics.get('likes', 0)
        comments = metrics.get('comments', 0)
        shares = metrics.get('shares', 0)
        saves = metrics.get('saves', 0)
        
        engagement_rate = ((likes + comments + shares + saves) / views) * 100
        return engagement_rate

    def calculate_watch_through_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate Watch-Through/Completion Rate.
        
        Formula: Watch-Through % = (average watch time / video length) × 100%
        
        Args:
            metrics: Dictionary containing average_watch_time and video_length
            
        Returns:
            Watch-through rate as a percentage (0-100)
        """
        video_length = metrics.get('video_length', 0)
        if video_length == 0:
            return 0.0
        
        average_watch_time = metrics.get('average_watch_time', 0)
        watch_through_rate = (average_watch_time / video_length) * 100
        return min(watch_through_rate, 100.0)

    def calculate_conversion_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate Conversion Rate (CR).
        
        Formula: CR = conversions (subs, follows, clicks, signups) / views × 100%
        
        Args:
            metrics: Dictionary containing views and conversions
            
        Returns:
            Conversion rate as a percentage (0-100)
        """
        views = metrics.get('views', 0)
        if views == 0:
            return 0.0
        
        conversions = metrics.get('conversions', 0)
        conversion_rate = (conversions / views) * 100
        return conversion_rate

    def calculate_relative_performance_index(self, metrics: Dict[str, Any], 
                                            metric_name: str = 'views') -> float:
        """Calculate Relative Performance Index (RPI).
        
        Formula: RPI = (current video metric / channel median) × 100%
        
        Args:
            metrics: Dictionary containing the metric and channel_median_{metric}
            metric_name: Name of the metric to compare (default: 'views')
            
        Returns:
            RPI as a percentage (can exceed 100)
        """
        current_value = metrics.get(metric_name, 0)
        median_key = f'channel_median_{metric_name}'
        channel_median = metrics.get(median_key, 0)
        
        if channel_median == 0:
            return 0.0
        
        rpi = (current_value / channel_median) * 100
        return rpi

    def calculate_universal_content_score(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate Universal Content Score (UCS) and component metrics.
        
        UCS Formula:
        UCS = 0.4 × Engagement Rate + 
              0.4 × Watch-Through Rate + 
              0.2 × RPI (views vs channel median)
        
        Args:
            metrics: Dictionary containing all necessary metrics
            
        Returns:
            Dictionary containing UCS and all component scores
        """
        # Calculate component metrics
        engagement_rate = self.calculate_engagement_rate(metrics)
        watch_through_rate = self.calculate_watch_through_rate(metrics)
        rpi_views = self.calculate_relative_performance_index(metrics, 'views')
        
        # Normalize RPI to 0-100 scale (cap at 200% for scoring purposes)
        normalized_rpi = min(rpi_views, 200.0) / 2.0
        
        # Calculate UCS
        ucs = (0.4 * engagement_rate + 
               0.4 * watch_through_rate + 
               0.2 * normalized_rpi)
        
        return {
            'universal_content_score': min(ucs, 100.0),
            'engagement_rate': engagement_rate,
            'watch_through_rate': watch_through_rate,
            'relative_performance_index': rpi_views,
            'conversion_rate': self.calculate_conversion_rate(metrics)
        }
