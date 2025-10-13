# YouTube Channel Scraping Guide

This guide explains how to use the YouTube channel scraping feature to collect comprehensive metadata from YouTube Shorts.

## Overview

The channel scraping feature uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to extract detailed metadata from YouTube channel Shorts, providing much more information than the standard YouTube API search.

## Features

### What Channel Scraping Provides

- **Subtitle Extraction**: Automatically downloads and parses video subtitles
- **Video Quality Metrics**: Resolution, FPS, and aspect ratio
- **Engagement Analytics**: 
  - Views per day/hour since upload
  - Engagement rate (likes + comments / views)
  - Like-to-view and comment-to-view ratios
- **Channel Information**: Channel ID, name, and subscriber count
- **Content Analysis**: Title length, description length, tag counts

### Advantages Over API Search

| Feature | Channel Scraping (yt-dlp) | API Search |
|---------|---------------------------|------------|
| Subtitles | ✅ Full text extraction | ❌ Not available |
| Video Quality | ✅ Resolution, FPS, aspect ratio | ❌ Limited |
| Engagement Analytics | ✅ Views per day/hour | ❌ Not available |
| API Quota | ✅ No limits | ❌ 10,000 units/day |
| Channel Filtering | ✅ Precise channel targeting | ⚠️ Search-based only |
| Setup Required | yt-dlp installation | YouTube API key |

## Installation

Channel scraping requires yt-dlp to be installed. It's already included in the requirements.txt:

```bash
pip install -r requirements.txt
```

Or install yt-dlp separately:

```bash
pip install yt-dlp
```

## Basic Usage

### Scrape from a Channel

```bash
# Using channel handle
python -m src.cli scrape-channel --channel @channelname

# Using full channel URL
python -m src.cli scrape-channel --channel https://www.youtube.com/@channelname

# Using channel ID
python -m src.cli scrape-channel --channel UC1234567890
```

### Limit Number of Shorts

```bash
# Scrape only 5 shorts
python -m src.cli scrape-channel --channel @channelname --top 5

# Scrape 20 shorts
python -m src.cli scrape-channel --channel @channelname --top 20
```

## Configuration

### Environment Variables

Configure channel scraping in your `.env` file:

```ini
# YouTube Channel Configuration
YOUTUBE_CHANNEL_URL=@your_channel_name
YOUTUBE_CHANNEL_MAX_SHORTS=10
```

Then run without arguments:

```bash
python -m src.cli scrape-channel
```

### CLI Options Override Config

CLI options take precedence over environment variables:

```bash
# Override config settings
python -m src.cli scrape-channel --channel @otherchannel --top 15
```

## Enhanced Metrics

Channel scraping provides enhanced metrics stored in the `enhanced_metrics` section:

```json
{
  "enhanced_metrics": {
    "engagement_rate": 6.5,
    "views_per_day": 1234.5,
    "resolution": "1080x1920",
    "fps": 30,
    "aspect_ratio": "1080:1920",
    "subtitle_text": "Full subtitle text extracted...",
    "subtitles_available": true,
    "channel_follower_count": 150000
  }
}
```

## Shorts Filtering

Channel scraping applies strict filtering to ensure only true Shorts are collected:

1. **Duration**: ≤ 180 seconds (3 minutes)
2. **Format**: Vertical aspect ratio (height > width)

Videos that don't meet these criteria are automatically skipped.

## Performance Considerations

### Scraping Speed

- **Average time per video**: 3-5 seconds
- **10 shorts**: ~30-50 seconds
- **20 shorts**: ~60-100 seconds

Time includes:
- Metadata extraction
- Subtitle downloading

### Bandwidth Usage

- Minimal bandwidth (metadata only)
- Subtitle files are small (typically < 10 KB)
- No video files are downloaded

## Troubleshooting

### yt-dlp Not Found

```
Error: yt-dlp is not installed
Install with: pip install yt-dlp
```

**Solution**: Install yt-dlp:
```bash
pip install yt-dlp
```

### No Shorts Found

```
No shorts found for channel: https://www.youtube.com/@channelname
```

**Possible causes**:
- Channel has no Shorts
- Channel URL is incorrect
- Shorts tab may not be accessible

**Solution**: 
- Verify the channel has a Shorts tab
- Try different URL formats (@handle, channel ID, full URL)

## Best Practices

### Choosing Channels

1. **Check Shorts availability**: Ensure the channel has a Shorts tab
2. **Verify recent activity**: Recent uploads provide better engagement metrics

### Optimizing Results

1. **Start small**: Begin with `--top 5` to test
2. **Check subtitles**: Channels with good subtitles provide better metadata
3. **Monitor engagement**: Higher engagement videos often have better subtitles

### Integration with PrismQ Ecosystem

Channel scraping integrates seamlessly with other PrismQ modules:

1. **Database**: All scraped data stored in SQLite
2. **Metrics**: Universal metrics compatible with other sources
3. **Export**: Data can be exported for StoryGenerator and other tools

## Examples

### Example 1: Analyze Channel Performance

```bash
# Scrape recent Shorts to analyze engagement
python -m src.cli scrape-channel \
  --channel @yourchannel \
  --top 10

# Then view statistics
python -m src.cli stats
```

### Example 2: Compare Multiple Channels

```bash
# Scrape from multiple channels
python -m src.cli scrape-channel --channel @channel1 --top 10
python -m src.cli scrape-channel --channel @channel2 --top 10
python -m src.cli scrape-channel --channel @channel3 --top 10

# View all collected ideas
python -m src.cli list --limit 30
```

## Advanced Usage

### Accessing Enhanced Metrics Programmatically

```python
from src.database import Database
from src.config import Config

config = Config()
db = Database(config.database_path)

# Get ideas with enhanced metrics
ideas = db.get_all_ideas(limit=10)

for idea in ideas:
    # Access enhanced metrics
    metrics = idea['score_dictionary']
    enhanced = metrics.get('enhanced_metrics', {})
    
    print(f"Title: {idea['title']}")
    print(f"  Engagement Rate: {enhanced.get('engagement_rate', 0)}%")
    print(f"  Views/Day: {enhanced.get('views_per_day', 0)}")
```

## See Also

- [Main README](../README.md)
- [Metrics Documentation](METRICS.md)
- [Contributing Guidelines](CONTRIBUTING.md)
