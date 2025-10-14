# Data Collection Quick Reference

> 📘 **See [DATA_COLLECTION_ANALYSIS.md](DATA_COLLECTION_ANALYSIS.md) for comprehensive details**

## What We Collect Now ✅

### Core Metrics
- ✅ **Engagement**: Views, likes, comments, favorites
- ✅ **Content**: Title, description, tags, subtitles (yt-dlp)
- ✅ **Quality**: Resolution, FPS, aspect ratio (yt-dlp)
- ✅ **Channel**: Name, ID, subscriber count (yt-dlp)
- ✅ **Analytics**: Engagement rate, views per day/hour (calculated)

### Collection Methods

| Method | Pros | Recommended |
|--------|------|-------------|
| **yt-dlp (channel)** | Rich metadata, subtitles, no quota, comprehensive data | ✅ Primary |
| **yt-dlp (trending)** | Discover viral content, same rich metadata | ✅ Yes |
| **yt-dlp (keyword)** | Flexible search, same rich metadata | ✅ Yes |

## What We Can Add Easily 🟢

### High Priority (Already in API response, no extra cost)
1. **Video Quality Flags**
   - HD/SD definition
   - Caption availability (boolean)
   - 2D/3D dimension

2. **Status Information** (+2 quota)
   - Privacy status (public/unlisted)
   - Embeddable flag
   - Made for kids indicator

3. **From yt-dlp** (No extra cost)
   - Hashtags (extracted)
   - Channel verification status
   - Thumbnail URLs
   - Video bitrate

### Medium Priority (Requires extra API call)
1. **Topic Categories** (+2 quota)
   - Topic IDs
   - Wikipedia topic links
   - Better categorization

2. **Recording Details** (+2 quota)
   - Location (if available)
   - Recording date
   - Geo-coordinates

## What's Possible in Future 🟡

### GPU-Accelerated Analysis (RTX 5090)
- 🎥 **Visual**: Scene detection, object recognition, text extraction
- 🎵 **Audio**: Music detection, speech clarity, audio quality
- 📝 **NLP**: Sentiment analysis, clickbait detection, topic modeling
- 📈 **Trends**: Viral probability, growth prediction

## What's NOT Accessible ❌

- ❌ Detailed analytics (requires channel ownership)
- ❌ Watch time, audience retention
- ❌ Accurate dislike counts (hidden by YouTube)
- ❌ Real-time recommendation scores
- ❌ Traffic sources, demographics
- ❌ Revenue data

## Current Data Size

Per idea:
- **Current**: 2-5 KB (40+ metrics)
- **With additions**: 3-8 KB
- **Storage for 100K ideas**: 300-800 MB (very manageable)

## No Quota Restrictions

**yt-dlp collection:**
- **No quota limits**: Unlimited videos per day
- **No restrictions**: All fields available without API quotas
- **Flexible**: Collect as much data as needed

## Quick Decision Guide

### Collection Method: yt-dlp

**yt-dlp provides comprehensive data collection:**
- ✅ Complete metadata: title, description, tags, views, likes, comments
- ✅ Subtitles: full text extraction
- ✅ Quality metrics: resolution, FPS, aspect ratio, codecs
- ✅ Channel data: subscriber count, verification status
- ✅ Analytics: engagement rate, views per day/hour
- ✅ Unlimited: no quota restrictions

**Use yt-dlp for:**
- ✅ All data collection needs
- ✅ Bulk collection without limits
- ✅ Channel, trending, and keyword scraping
- ✅ Comprehensive metadata including subtitles

### What data should I add next?

```
1. 🟢 Start with: contentDetails flags (HD, captions)
2. 🟢 Then add: status information (privacy, embeddable)
3. 🟢 Easy wins: hashtags from yt-dlp
4. 🟡 Consider: topic categories
5. 🟡 Future: GPU-based content analysis
```

## Schema Overview

```python
UniversalMetrics:
    # Engagement (40% of fields)
    - view_count, like_count, comment_count, share_count
    - engagement_rate, like_to_view_ratio, etc.
    
    # Content (30% of fields)
    - title, description, tags, subtitles
    - duration, quality metrics
    
    # Channel (15% of fields)
    - channel info, subscriber count, verification
    
    # Platform (15% of fields)
    - platform type, content type
    - upload date, categories
    
    # Raw data
    - platform_specific: Dict (preserves all original data)
```

## Examples

### What's Collected (yt-dlp)
```json
{
  "view_count": 1500000,
  "like_count": 75000,
  "comment_count": 2500,
  "resolution": "1080x1920",
  "fps": 30,
  "subtitles": "Full subtitle text here...",
  "engagement_rate": 5.17,
  "views_per_day": 50000,
  "channel_follower_count": 500000
}
```

### What Could Be Added
```json
{
  "definition": "hd",
  "has_captions": true,
  "privacy_status": "public",
  "embeddable": true,
  "made_for_kids": false,
  "hashtags": ["#shorts", "#viral"],
  "channel_verified": true,
  "thumbnail_url": "https://...",
  "video_bitrate": 2500
}
```

### Future Possibilities
```json
{
  "visual_analysis": {
    "faces_detected": 2,
    "text_on_screen": ["SUBSCRIBE"],
    "aesthetic_score": 0.82
  },
  "audio_analysis": {
    "music_detected": true,
    "speech_clarity": 0.88
  },
  "nlp_analysis": {
    "sentiment_score": 0.75,
    "clickbait_score": 0.45
  }
}
```

## Next Steps

1. **Review** [DATA_COLLECTION_ANALYSIS.md](DATA_COLLECTION_ANALYSIS.md) for full details
2. **Decide** which additional fields to collect
3. **Update** UniversalMetrics schema if needed
4. **Test** with sample data
5. **Deploy** changes incrementally

---

**Last Updated**: 2025-10-13  
**Current Version**: 1.0.0
