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
- **Story Detection**: AI-powered classification of story-based content
- **Channel Information**: Channel ID, name, and subscriber count
- **Content Analysis**: Title length, description length, tag counts

### Advantages Over API Search

| Feature | Channel Scraping (yt-dlp) | API Search |
|---------|---------------------------|------------|
| Subtitles | ✅ Full text extraction | ❌ Not available |
| Video Quality | ✅ Resolution, FPS, aspect ratio | ❌ Limited |
| Engagement Analytics | ✅ Views per day/hour | ❌ Not available |
| Story Detection | ✅ AI-powered analysis | ❌ Not available |
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

### Story-Only Mode

Filter for story-based videos only:

```bash
# Only scrape videos detected as stories
python -m src.cli scrape-channel --channel @channelname --story-only
```

## Configuration

### Environment Variables

Configure channel scraping in your `.env` file:

```ini
# YouTube Channel Configuration
YOUTUBE_CHANNEL_URL=@your_channel_name
YOUTUBE_CHANNEL_MAX_SHORTS=10
YOUTUBE_CHANNEL_STORY_ONLY=false
```

Then run without arguments:

```bash
python -m src.cli scrape-channel
```

### CLI Options Override Config

CLI options take precedence over environment variables:

```bash
# Override config settings
python -m src.cli scrape-channel --channel @otherchannel --top 15 --story-only
```

## Story Detection

The story detector analyzes video metadata to classify content as story-based or not.

### How It Works

Story detection uses weighted keyword analysis across:

1. **Title Keywords** (weighted 1-3):
   - High confidence: "story", "storytime", "aita", "confession"
   - Medium confidence: "relationship", "drama", "toxic", "karen"
   - Low confidence: "experience", "happened", "crazy"

2. **Description Keywords**:
   - "story", "true story", "my story", "happened to me"

3. **Tags**:
   - "storytime", "true story", "reddit story", "confession"

4. **Subtitle Analysis**:
   - First-person narrative indicators
   - "I was", "I had", "this happened"

### Confidence Scoring

- **Score Range**: 0.0 to 1.0
- **Default Threshold**: 0.3
- **Classification**: Scores ≥ 0.3 are classified as stories

### Anti-Patterns

Videos are automatically excluded if they contain:
- Tutorial keywords: "how to", "tutorial", "guide"
- Gameplay keywords: "gameplay", "walkthrough"
- Review keywords: "review", "unboxing", "haul"
- Other: "reaction", "news", "announcement"

### Example Output

```
[1/10] Extracting metadata for: dQw4w9WgXcQ
    ✅ Extracted (🎬 short): My AITA Story - Was I Wrong? [00:45]
    📖 Story: Yes (confidence: 0.85)
    📊 Engagement Rate: 6.5%
    👁️ Views per day: 1,234

[2/10] Extracting metadata for: abc123xyz
    ✅ Extracted (🎬 short): How to Make Videos - Tutorial [01:30]
    📖 Story: No (anti-pattern detected: tutorial)
    📊 Engagement Rate: 3.2%
    👁️ Views per day: 567
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
    "channel_follower_count": 150000,
    "is_story_video": true,
    "story_confidence_score": 0.85,
    "story_indicators": [
      "title: story",
      "description: happened to me",
      "tag: storytime"
    ]
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
- Story detection analysis

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

### Story-Only Mode Returns No Results

If `--story-only` returns no videos:
- The channel may not have story-based content
- Try running without `--story-only` first to see what's available
- Check story confidence scores in the output

## Best Practices

### Choosing Channels

1. **Target story-focused channels**: Channels that create narrative content
2. **Check Shorts availability**: Ensure the channel has a Shorts tab
3. **Verify recent activity**: Recent uploads provide better engagement metrics

### Optimizing Results

1. **Start small**: Begin with `--top 5` to test
2. **Use story filtering**: Add `--story-only` for narrative content
3. **Check subtitles**: Channels with good subtitles provide better story detection
4. **Monitor engagement**: Higher engagement videos often have better subtitles

### Integration with PrismQ Ecosystem

Channel scraping integrates seamlessly with other PrismQ modules:

1. **Database**: All scraped data stored in SQLite
2. **Metrics**: Universal metrics compatible with other sources
3. **Story Detection**: Consistent across content types
4. **Export**: Data can be exported for StoryGenerator and other tools

## Examples

### Example 1: Scrape Story Content

```bash
# Find story-based Shorts from a channel
python -m src.cli scrape-channel \
  --channel @storytimechannel \
  --top 20 \
  --story-only
```

### Example 2: Analyze Channel Performance

```bash
# Scrape recent Shorts to analyze engagement
python -m src.cli scrape-channel \
  --channel @yourchannel \
  --top 10

# Then view statistics
python -m src.cli stats
```

### Example 3: Compare Multiple Channels

```bash
# Scrape from multiple channels
python -m src.cli scrape-channel --channel @channel1 --top 10
python -m src.cli scrape-channel --channel @channel2 --top 10
python -m src.cli scrape-channel --channel @channel3 --top 10

# View all collected ideas
python -m src.cli list --limit 30
```

### Example 4: Find High-Engagement Stories

```bash
# Scrape story content
python -m src.cli scrape-channel \
  --channel @popularchannel \
  --top 20 \
  --story-only

# View by engagement rate (stored in score field)
python -m src.cli list --limit 10
```

## Advanced Usage

### Custom Story Detection Threshold

Story detection uses a default threshold of 0.3. To customize, you can:

1. Modify the threshold in code (src/story_detector.py)
2. Filter results after scraping based on story_confidence_score

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
    print(f"  Story: {enhanced.get('is_story_video', False)}")
    print(f"  Confidence: {enhanced.get('story_confidence_score', 0)}")
```

## See Also

- [Main README](../README.md)
- [Metrics Documentation](METRICS.md)
- [Contributing Guidelines](CONTRIBUTING.md)
