# Universal Metrics Documentation

## Overview

PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource uses a **universal metrics schema** that standardizes data collection from YouTube Shorts. This schema is designed to be compatible with other PrismQ Idea Sources modules for cross-platform analysis:
- YouTube Shorts (this module)
- TikTok (separate module)
- Instagram Reels (separate module)
- Reddit (separate module)
- Other platforms (as separate modules)

This approach enables consistent analysis and comparison of content performance across different platforms in the PrismQ ecosystem.

## Core Metrics Collected

### Engagement Metrics
All platforms provide these core metrics (when available):

| Metric | Description | Platforms |
|--------|-------------|-----------|
| `view_count` | Total views/impressions | All |
| `like_count` | Likes/upvotes/reactions | All |
| `comment_count` | Number of comments | All |
| `share_count` | Shares/reposts | YouTube, Instagram, TikTok, Facebook |

### Platform-Specific Metrics

Additional metrics available from specific platforms:

| Metric | Description | Platform |
|--------|-------------|----------|
| `upvote_count` | Reddit upvotes | Reddit |
| `downvote_count` | Reddit downvotes | Reddit |
| `upvote_ratio` | Ratio of upvotes to total votes | Reddit |
| `dislike_count` | YouTube dislikes (often hidden) | YouTube |
| `favorite_count` | YouTube favorites | YouTube |
| `save_count` | Instagram saves | Instagram |
| `repost_count` | TikTok reposts | TikTok |

### Calculated Engagement Metrics

The system automatically calculates derived engagement metrics:

| Metric | Formula | Purpose |
|--------|---------|---------|
| `engagement_rate` | `(likes + comments + shares) / views × 100` | Overall audience interaction percentage |
| `like_to_view_ratio` | `likes / views × 100` | Positive sentiment indicator |
| `comment_to_view_ratio` | `comments / views × 100` | Discussion activity level |
| `share_to_view_ratio` | `shares / views × 100` | Virality indicator |

### Performance Metrics

Time-based performance indicators:

| Metric | Description |
|--------|-------------|
| `views_per_day` | Average daily view count since upload |
| `views_per_hour` | Granular hourly view rate |
| `days_since_upload` | Age of content in days |

### Content Quality Indicators

Metadata about content quality:

| Metric | Description |
|--------|-------------|
| `title_length` | Number of characters in title |
| `description_length` | Number of characters in description |
| `tag_count` | Number of tags/hashtags |
| `has_subtitles` | Whether subtitles are available |
| `has_chapters` | Whether video has chapter markers |
| `chapter_count` | Number of chapters |
| `resolution` | Video resolution (e.g., "1920x1080") |
| `fps` | Frames per second |
| `aspect_ratio` | Video aspect ratio (e.g., "16:9", "9:16") |

### Channel/Author Metrics

Creator-level metrics:

| Metric | Description |
|--------|-------------|
| `author_follower_count` | Total subscribers/followers |
| `author_verification` | Whether account is verified |

## Data Storage

Metrics are stored in the database in two ways:

1. **Engagement Rate as Score**: The calculated `engagement_rate` is stored in the `score` field for easy sorting and comparison
2. **Full Metrics Dictionary**: All metrics are stored in the `score_dictionary` field as JSON, preserving all platform-specific data

## Usage Example

```python
from src.metrics import UniversalMetrics

# From YouTube
youtube_data = {...}  # YouTube API response
metrics = UniversalMetrics.from_youtube(youtube_data)

# From Reddit
reddit_post = {...}  # Reddit post data
metrics = UniversalMetrics.from_reddit(reddit_post)

# Calculate derived metrics
metrics.calculate_derived_metrics()

# Access metrics
print(f"Engagement Rate: {metrics.engagement_rate}%")
print(f"Views per Day: {metrics.views_per_day}")

# Convert to dictionary for storage
metrics_dict = metrics.to_dict()
```

## Platform-Specific Implementations

### YouTube Shorts (This Module)
Uses the full YouTube API response to extract:
- View, like, comment, favorite counts
- Video duration, resolution, FPS
- Title, description, tags
- Channel information
- Upload date
- Filters for videos up to 3 minutes (180 seconds)

### Other Platforms (Separate Modules)
Other PrismQ Idea Sources modules implement similar patterns:
- `PrismQ.IdeaInspiration.Sources.Content.Forums.RedditSource` - Reddit posts
- `PrismQ.IdeaInspiration.Sources.Content.Shorts.TikTokSource` - TikTok videos
- `PrismQ.IdeaInspiration.Sources.Content.Shorts.InstagramReelsSource` - Instagram Reels
- etc.

Each module implements the universal metrics schema for cross-platform compatibility.

## Benefits of Universal Metrics

1. **Cross-Platform Comparison**: Compare content performance across different platforms using standardized metrics
2. **Flexible Storage**: Platform-specific data preserved in `platform_specific` field
3. **Extensibility**: Easy to add new platforms by implementing new `from_*` factory methods
4. **Analytics Ready**: Calculated metrics ready for reporting and analysis
5. **Future-Proof**: Designed to accommodate new platforms and metrics as they become available

## Benchmarks

### Engagement Rate Benchmarks
- **Excellent**: > 5%
- **Good**: 2-5%
- **Average**: 1-2%
- **Low**: < 1%

### Like-to-View Ratio Benchmarks
- **Industry Average**: 2-4%
- **Good Performance**: > 4%

## Adding Support for Other Platforms

To add support for new platforms, create separate repositories following the PrismQ Idea Sources taxonomy:

1. Create a new repository (e.g., `PrismQ.IdeaInspiration.Sources.Content.Shorts.TikTokSource`)
2. Implement a `from_<platform>()` class method in `UniversalMetrics`
3. Map platform-specific fields to universal schema
4. Store any unique platform data in `platform_specific` field

Example for a TikTok module:
```python
@classmethod
def from_tiktok(cls, video_data: Dict[str, Any]) -> 'UniversalMetrics':
    stats = video_data.get('stats', {})
    
    metrics = cls(
        platform="tiktok",
        view_count=stats.get('playCount', 0),
        like_count=stats.get('diggCount', 0),
        comment_count=stats.get('commentCount', 0),
        share_count=stats.get('shareCount', 0),
        platform_specific=video_data  # Preserve TikTok-specific data
    )
    
    metrics.calculate_derived_metrics()
    return metrics
```

See the [PrismQ.RepositoryTemplate](https://github.com/Nomoos/PrismQ.RepositoryTemplate) for module structure guidelines.
