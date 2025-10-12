"""Universal metrics schema for cross-platform idea collection.

This module defines a standardized metrics structure that works across
multiple platforms: YouTube, Reddit, Facebook, Instagram, TikTok, etc.

Inspired by comprehensive analytics tools like VidIQ and TubeBuddy.
"""

from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class UniversalMetrics:
    """Universal metrics schema for cross-platform content analysis.
    
    This schema standardizes metrics across different platforms to enable
    consistent analysis and comparison.
    """
    
    # === Core Engagement Metrics ===
    # These are the primary metrics available on most platforms
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    
    # === Platform-Specific Engagement ===
    dislike_count: Optional[int] = None  # YouTube (often hidden)
    upvote_count: Optional[int] = None   # Reddit ups
    downvote_count: Optional[int] = None # Reddit downs
    favorite_count: Optional[int] = None # YouTube favorites
    save_count: Optional[int] = None     # Instagram saves
    repost_count: Optional[int] = None   # TikTok reposts
    
    # === Engagement Ratios ===
    # Calculated engagement metrics
    upvote_ratio: Optional[float] = None         # Reddit upvote ratio
    engagement_rate: Optional[float] = None      # (likes + comments + shares) / views
    like_to_view_ratio: Optional[float] = None   # likes / views
    comment_to_view_ratio: Optional[float] = None # comments / views
    share_to_view_ratio: Optional[float] = None  # shares / views
    
    # === Performance Metrics ===
    # Time-based performance indicators
    views_per_day: Optional[float] = None
    views_per_hour: Optional[float] = None
    days_since_upload: Optional[int] = None
    
    # === Content Metadata ===
    duration_seconds: Optional[int] = None       # Video/content duration
    title_length: Optional[int] = None           # Character count
    description_length: Optional[int] = None     # Character count
    tag_count: Optional[int] = None              # Number of tags/hashtags
    
    # === Quality Indicators ===
    has_subtitles: bool = False                  # Subtitle availability
    has_chapters: bool = False                   # Chapter markers (YouTube)
    chapter_count: Optional[int] = None
    resolution: Optional[str] = None             # Video resolution (e.g., "1920x1080")
    fps: Optional[int] = None                    # Frames per second
    aspect_ratio: Optional[str] = None           # e.g., "16:9", "9:16"
    
    # === Platform Context ===
    platform: str = "unknown"                    # youtube, reddit, instagram, tiktok, facebook
    content_type: Optional[str] = None           # short, long, post, story, reel, etc.
    
    # === Channel/Author Metrics ===
    author_follower_count: Optional[int] = None  # Channel subscribers/followers
    author_verification: bool = False            # Verified account status
    
    # === Additional Context ===
    upload_date: Optional[str] = None            # ISO format or platform format
    categories: List[str] = field(default_factory=list)
    age_restriction: Optional[int] = None        # 0 = none, 18 = adult
    
    # === Raw Platform Data ===
    # Store platform-specific data that doesn't fit standard schema
    platform_specific: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_derived_metrics(self):
        """Calculate derived metrics from raw data."""
        # Engagement rate: (likes + comments + shares) / views * 100
        if self.view_count > 0:
            total_engagement = self.like_count + self.comment_count + self.share_count
            self.engagement_rate = (total_engagement / self.view_count) * 100
            
            # Individual ratios
            self.like_to_view_ratio = (self.like_count / self.view_count) * 100
            self.comment_to_view_ratio = (self.comment_count / self.view_count) * 100
            if self.share_count > 0:
                self.share_to_view_ratio = (self.share_count / self.view_count) * 100
        
        # Performance metrics
        if self.days_since_upload and self.days_since_upload > 0:
            self.views_per_day = self.view_count / self.days_since_upload
            if self.views_per_day:
                self.views_per_hour = self.views_per_day / 24
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary, excluding None values."""
        result = asdict(self)
        # Remove None values for cleaner storage
        return {k: v for k, v in result.items() if v is not None and v != [] and v != {}}
    
    @classmethod
    def from_youtube(cls, video_data: Dict[str, Any], snippet: Dict[str, Any] = None, 
                     statistics: Dict[str, Any] = None) -> 'UniversalMetrics':
        """Create UniversalMetrics from YouTube API data.
        
        Args:
            video_data: Full video data from YouTube API
            snippet: Video snippet (optional if included in video_data)
            statistics: Video statistics (optional if included in video_data)
        """
        snippet = snippet or video_data.get('snippet', {})
        statistics = statistics or video_data.get('statistics', {})
        content_details = video_data.get('contentDetails', {})
        enhanced_metrics = video_data.get('enhanced_metrics', {})
        
        # Extract video quality metrics (from enhanced_metrics if available)
        resolution = enhanced_metrics.get('resolution')
        fps = enhanced_metrics.get('fps')
        aspect_ratio = enhanced_metrics.get('aspect_ratio')
        
        metrics = cls(
            platform="youtube",
            view_count=int(statistics.get('viewCount', 0)),
            like_count=int(statistics.get('likeCount', 0)),
            comment_count=int(statistics.get('commentCount', 0)),
            dislike_count=int(statistics.get('dislikeCount', 0)) if statistics.get('dislikeCount') else None,
            favorite_count=int(statistics.get('favoriteCount', 0)),
            
            # Content metadata
            title_length=len(snippet.get('title', '')),
            description_length=len(snippet.get('description', '')),
            tag_count=len(snippet.get('tags', [])),
            
            # Video quality metrics
            resolution=resolution,
            fps=fps,
            aspect_ratio=aspect_ratio,
            has_subtitles=enhanced_metrics.get('subtitles_available', False),
            
            # Channel metrics
            author_follower_count=enhanced_metrics.get('channel_follower_count'),
            
            # Platform data
            upload_date=snippet.get('publishedAt'),
            categories=[snippet.get('categoryId')] if snippet.get('categoryId') else [],
            
            # Store full data for reference
            platform_specific={
                'video_id': video_data.get('id'),
                'channel_id': snippet.get('channelId'),
                'channel_title': snippet.get('channelTitle'),
                'duration': content_details.get('duration'),
                'subtitle_text': enhanced_metrics.get('subtitle_text'),
                'engagement_rate': enhanced_metrics.get('engagement_rate'),
                'views_per_day': enhanced_metrics.get('views_per_day'),
            }
        )
        
        # Calculate derived metrics
        metrics.calculate_derived_metrics()
        
        return metrics
    
    @classmethod
    def from_reddit(cls, post_data: Dict[str, Any]) -> 'UniversalMetrics':
        """Create UniversalMetrics from Reddit post data.
        
        Args:
            post_data: Reddit post data (from PRAW or dict)
        """
        # Handle both PRAW objects and dictionaries
        if hasattr(post_data, '__dict__'):
            # PRAW object
            view_count = getattr(post_data, 'num_views', 0) or 0
            score = getattr(post_data, 'score', 0)
            ups = getattr(post_data, 'ups', 0)
            num_comments = getattr(post_data, 'num_comments', 0)
            upvote_ratio = getattr(post_data, 'upvote_ratio', 0)
            title = getattr(post_data, 'title', '')
            selftext = getattr(post_data, 'selftext', '')
        else:
            # Dictionary
            view_count = post_data.get('num_views', 0) or 0
            score = post_data.get('score', 0)
            ups = post_data.get('ups', 0)
            num_comments = post_data.get('num_comments', 0)
            upvote_ratio = post_data.get('upvote_ratio', 0)
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
        
        metrics = cls(
            platform="reddit",
            view_count=view_count,
            like_count=score,  # Reddit score as "likes"
            upvote_count=ups,
            comment_count=num_comments,
            upvote_ratio=upvote_ratio,
            
            # Content metadata
            title_length=len(title),
            description_length=len(selftext),
            
            # Store full data
            platform_specific={
                'score': score,
                'ups': ups,
                'upvote_ratio': upvote_ratio,
            }
        )
        
        # Calculate derived metrics
        metrics.calculate_derived_metrics()
        
        return metrics
    
    @classmethod
    def from_instagram(cls, post_data: Dict[str, Any]) -> 'UniversalMetrics':
        """Create UniversalMetrics from Instagram post data.
        
        Args:
            post_data: Instagram post data
        """
        metrics = cls(
            platform="instagram",
            like_count=post_data.get('like_count', 0),
            comment_count=post_data.get('comments_count', 0),
            save_count=post_data.get('saved_count', 0),
            share_count=post_data.get('share_count', 0),
            
            platform_specific=post_data
        )
        
        metrics.calculate_derived_metrics()
        return metrics
    
    @classmethod
    def from_tiktok(cls, video_data: Dict[str, Any]) -> 'UniversalMetrics':
        """Create UniversalMetrics from TikTok video data.
        
        Args:
            video_data: TikTok video data
        """
        stats = video_data.get('stats', {})
        
        metrics = cls(
            platform="tiktok",
            view_count=stats.get('playCount', 0),
            like_count=stats.get('diggCount', 0),
            comment_count=stats.get('commentCount', 0),
            share_count=stats.get('shareCount', 0),
            repost_count=stats.get('repostCount', 0),
            
            platform_specific=video_data
        )
        
        metrics.calculate_derived_metrics()
        return metrics
    
    @classmethod
    def from_facebook(cls, post_data: Dict[str, Any]) -> 'UniversalMetrics':
        """Create UniversalMetrics from Facebook post data.
        
        Args:
            post_data: Facebook post data
        """
        metrics = cls(
            platform="facebook",
            like_count=post_data.get('likes', {}).get('summary', {}).get('total_count', 0),
            comment_count=post_data.get('comments', {}).get('summary', {}).get('total_count', 0),
            share_count=post_data.get('shares', {}).get('count', 0),
            
            platform_specific=post_data
        )
        
        metrics.calculate_derived_metrics()
        return metrics
