# YouTube Shorts Data Collection Analysis

## Executive Summary

This document provides a comprehensive analysis of:
1. **What data we're currently collecting** from YouTube Shorts
2. **What additional data we can collect** from available APIs
3. **What's possible** with current technology and APIs

## Current Data Collection

### 1. Data We're Collecting Now

#### A. Through YouTube Data API v3 (Legacy Method)
The `youtube_plugin.py` currently collects:

**API Parts Requested:**
- `snippet` - Basic video information
- `statistics` - Engagement metrics  
- `contentDetails` - Video metadata

**Data Fields Collected:**

| Category | Field | Source | Status |
|----------|-------|--------|--------|
| **Engagement** | view_count | statistics.viewCount | ✅ Collected |
| **Engagement** | like_count | statistics.likeCount | ✅ Collected |
| **Engagement** | comment_count | statistics.commentCount | ✅ Collected |
| **Engagement** | dislike_count | statistics.dislikeCount | ✅ Collected (often hidden) |
| **Engagement** | favorite_count | statistics.favoriteCount | ✅ Collected |
| **Content** | title | snippet.title | ✅ Collected |
| **Content** | description | snippet.description | ✅ Collected |
| **Content** | tags | snippet.tags | ✅ Collected |
| **Content** | duration | contentDetails.duration | ✅ Collected (for filtering) |
| **Metadata** | title_length | Derived | ✅ Collected |
| **Metadata** | description_length | Derived | ✅ Collected |
| **Metadata** | tag_count | Derived | ✅ Collected |
| **Channel** | channel_id | snippet.channelId | ✅ Collected |
| **Channel** | channel_title | snippet.channelTitle | ✅ Collected |
| **Publishing** | publishedAt | snippet.publishedAt | ✅ Collected |
| **Publishing** | categoryId | snippet.categoryId | ✅ Collected |

#### B. Through yt-dlp (Enhanced Method) ⭐
The `youtube_channel_plugin.py`, `youtube_trending_plugin.py`, and keyword scraping collect:

**Enhanced Data Available:**

| Category | Field | Source | Status |
|----------|-------|--------|--------|
| **All API fields above** | - | - | ✅ Collected |
| **Video Quality** | resolution | Video stream metadata | ✅ Collected |
| **Video Quality** | fps (frames per second) | Video stream metadata | ✅ Collected |
| **Video Quality** | aspect_ratio | Video dimensions | ✅ Collected |
| **Content** | subtitles (full text) | Subtitle track extraction | ✅ Collected |
| **Content** | has_subtitles | Subtitle availability | ✅ Collected |
| **Analytics** | views_per_day | Calculated metric | ✅ Collected |
| **Analytics** | views_per_hour | Calculated metric | ✅ Collected |
| **Analytics** | engagement_rate | Calculated | ✅ Collected |
| **Analytics** | like_to_view_ratio | Calculated | ✅ Collected |
| **Analytics** | comment_to_view_ratio | Calculated | ✅ Collected |
| **Analytics** | share_to_view_ratio | Calculated | ✅ Collected |
| **Channel** | author_follower_count | Channel metadata | ✅ Collected |
| **Format** | format_id | Video format details | ✅ Collected |
| **Format** | vcodec | Video codec | ✅ Collected |
| **Format** | acodec | Audio codec | ✅ Collected |

### 2. Storage Schema

**Database Table: `ideas`**
```sql
CREATE TABLE ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    score REAL,                    -- Stores engagement_rate
    score_dictionary TEXT,          -- Full metrics as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, source_id)
);
```

**UniversalMetrics Schema:**
All collected data is stored in the `score_dictionary` field as JSON, containing:
- 40+ standardized metric fields
- Platform-specific data in `platform_specific` dictionary
- Calculated derived metrics

## What Additional Data Can We Collect?

### 1. Available from YouTube Data API v3 (Not Currently Collected)

#### Additional API Parts Available:

| API Part | Cost (Quota Units) | Data Provided | Priority |
|----------|-------------------|---------------|----------|
| `topicDetails` | +2 | Topic categories, Wikipedia URLs | 🟡 Medium |
| `localizations` | +2 | Translated titles/descriptions | 🟢 Low |
| `recordingDetails` | +2 | Recording location, date | 🟡 Medium |
| `liveStreamingDetails` | +2 | Live stream info (N/A for Shorts) | 🔴 Not Applicable |
| `player` | +0 | Embed HTML | 🔴 Not Useful |
| `status` | +2 | Privacy status, license, embeddable | 🟡 Medium |
| `fileDetails` | +1 | Video file metadata (requires ownership) | 🔴 Not Accessible |
| `processingDetails` | +1 | Processing status (requires ownership) | 🔴 Not Accessible |
| `suggestions` | +1 | Improvement suggestions (requires ownership) | 🔴 Not Accessible |

#### Specific Fields We Could Add:

**From `topicDetails` (Useful for content categorization):**
```json
{
  "topicDetails": {
    "topicIds": ["/m/02mjmr", "/m/01k8wb"],
    "relevantTopicIds": ["/m/098wr"],
    "topicCategories": [
      "https://en.wikipedia.org/wiki/Fashion",
      "https://en.wikipedia.org/wiki/Lifestyle_(sociology)"
    ]
  }
}
```

**From `recordingDetails` (Useful for location-based analysis):**
```json
{
  "recordingDetails": {
    "recordingDate": "2023-10-15T14:30:00Z",
    "location": {
      "latitude": 37.42307,
      "longitude": -122.08427,
      "altitude": 0
    },
    "locationDescription": "Googleplex, Mountain View, CA"
  }
}
```

**From `status` (Useful for content filtering):**
```json
{
  "status": {
    "uploadStatus": "processed",
    "privacyStatus": "public",
    "license": "youtube",
    "embeddable": true,
    "publicStatsViewable": true,
    "madeForKids": false,
    "selfDeclaredMadeForKids": false
  }
}
```

**From `contentDetails` (Already requested but not all fields extracted):**
```json
{
  "contentDetails": {
    "duration": "PT2M15S",
    "dimension": "2d",              // ❌ Not collected
    "definition": "hd",              // ❌ Not collected
    "caption": "true",               // ❌ Not collected (has captions?)
    "licensedContent": true,         // ❌ Not collected
    "contentRating": {},             // ❌ Not collected
    "projection": "rectangular",     // ❌ Not collected
    "hasCustomThumbnail": true       // ❌ Not collected (requires ownership)
  }
}
```

### 2. Available Through yt-dlp (Extensive Metadata)

yt-dlp provides access to hundreds of fields. Here are the most valuable ones we're NOT collecting:

#### A. Thumbnail Data
```python
{
  "thumbnails": [
    {
      "url": "https://...",
      "width": 1280,
      "height": 720,
      "preference": 1
    }
  ],
  "thumbnail": "https://..."  # Best thumbnail URL
}
```

#### B. Format Details (Detailed)
```python
{
  "formats": [
    {
      "format_id": "233",
      "ext": "mp4",
      "width": 1080,
      "height": 1920,
      "fps": 30,
      "vcodec": "avc1.64002a",
      "acodec": "mp4a.40.2",
      "vbr": 2500.0,              # ❌ Video bitrate
      "abr": 128.0,               # ❌ Audio bitrate
      "filesize": 15728640,       # ❌ File size
      "quality": 1,
      "tbr": 2628.0               # ❌ Total bitrate
    }
  ]
}
```

#### C. Audio/Music Information
```python
{
  "track": "Song Name",           # ❌ Music track name
  "artist": "Artist Name",        # ❌ Music artist
  "album": "Album Name",          # ❌ Album
  "release_date": "20230101",     # ❌ Music release date
  "release_year": 2023            # ❌ Release year
}
```

#### D. Advanced Engagement Metrics
```python
{
  "view_count": 1000000,
  "like_count": 50000,
  "dislike_count": 500,           # Usually unavailable
  "average_rating": 4.8,          # ❌ Average rating (deprecated)
  "comment_count": 1500,
  "age_limit": 0,                 # ✅ Collected as age_restriction
  "is_live": false,
  "was_live": false,
  "live_status": "not_live",      # ❌ Live status
  "playable_in_embed": true,      # ❌ Embeddable
  "availability": "public"        # ❌ Availability status
}
```

#### E. Channel Extended Info
```python
{
  "channel_id": "UC...",
  "channel": "Channel Name",
  "channel_follower_count": 1000000,  # ✅ Collected
  "uploader_id": "@channelhandle",    # ❌ Channel handle
  "uploader_url": "https://...",      # ❌ Channel URL
  "channel_is_verified": true         # ❌ Verification status
}
```

#### F. Location & Language
```python
{
  "language": "en",               # ❌ Primary language
  "subtitles": {                  # ✅ Collected (converted to text)
    "en": [...],
    "es": [...]
  },
  "automatic_captions": {         # ❌ Auto-generated captions
    "en": [...]
  }
}
```

#### G. Timing & Performance
```python
{
  "timestamp": 1609459200,        # ❌ Unix timestamp
  "upload_date": "20210101",      # ✅ Collected as publishedAt
  "modified_timestamp": 1609545600, # ❌ Last modified
  "modified_date": "20210102",    # ❌ Last modified date
  "release_timestamp": 1609459200 # ❌ Scheduled release time
}
```

#### H. Hashtags & Categories
```python
{
  "tags": ["tag1", "tag2"],       # ✅ Collected
  "categories": ["Education"],    # ✅ Collected (categoryId)
  "hashtags": ["#shorts", "#viral"], # ❌ Extracted hashtags
  "cast": [],                     # ❌ Cast members (if any)
  "genre": ["Music"]              # ❌ Genre
}
```

### 3. What Data is NOT Accessible

#### Restricted by YouTube:
1. **Detailed Analytics** (requires channel ownership):
   - Watch time
   - Audience retention graphs
   - Traffic sources
   - Demographics (age, gender, location of viewers)
   - Impressions and click-through rate
   - Revenue data

2. **Removed Features**:
   - Dislike counts (hidden since 2021, only visible to creator)
   - Detailed ratings

3. **Private/Unlisted Videos**:
   - Cannot scrape without proper access

4. **Copyrighted Content Detection**:
   - Content ID matches
   - Copyright claims

#### Technical Limitations:
1. **Real-time Data**:
   - View velocity (views per minute right now)
   - Current position in trending/recommendations
   
2. **Recommendation Algorithm**:
   - Why video was recommended
   - Recommendation score/ranking

3. **User Interaction History**:
   - Whether specific users watched/liked
   - Watch history patterns

## What's Possible with Advanced Techniques?

### 1. Computer Vision Analysis (Future Enhancement)

With the RTX 5090 GPU available, we could add:

```python
# Potential future features
{
  "visual_analysis": {
    "faces_detected": 2,
    "scene_changes": 15,
    "text_on_screen": ["SUBSCRIBE", "Like & Share"],
    "colors_dominant": ["#FF0000", "#00FF00"],
    "brightness_avg": 0.65,
    "objects_detected": ["person", "smartphone", "laptop"],
    "aesthetic_score": 0.82
  }
}
```

### 2. Audio Analysis (Future Enhancement)

```python
{
  "audio_analysis": {
    "music_detected": true,
    "speech_detected": true,
    "background_noise_level": 0.15,
    "speech_clarity": 0.88,
    "audio_quality_score": 0.75,
    "tempo_bpm": 120,
    "music_genre": "electronic"
  }
}
```

### 3. Natural Language Processing (Future Enhancement)

```python
{
  "nlp_analysis": {
    "sentiment_score": 0.75,        # Positive/negative
    "readability_score": 65,        # Flesch reading ease
    "keyword_density": {...},
    "entities_mentioned": ["Tesla", "Elon Musk"],
    "topics_detected": ["technology", "business"],
    "clickbait_score": 0.45,
    "urgency_indicators": ["NOW", "MUST SEE"]
  }
}
```

### 4. Trend Analysis (Future Enhancement)

```python
{
  "trend_analysis": {
    "growth_rate_24h": 150.5,      # % growth
    "viral_probability": 0.78,
    "similar_videos_count": 1500,
    "trend_category": "rising",
    "predicted_peak_views": 500000,
    "competition_level": "medium"
  }
}
```

## Recommendations

### Priority 1: Quick Wins (Low Effort, High Value)

1. **Add `contentDetails` fields** ✅ Recommended
   - `definition` (sd/hd)
   - `caption` (has captions boolean)
   - `dimension` (2d/3d)
   - Cost: Already included in current API call (no extra quota)

2. **Add `status` part** ✅ Recommended
   - Privacy status
   - Embeddable flag
   - Made for kids flag
   - Cost: +2 quota units per video

3. **Extract hashtags from yt-dlp** ✅ Recommended
   - Already available in yt-dlp response
   - No additional API cost
   - Useful for trend analysis

4. **Add channel verification status** ✅ Recommended
   - Available in yt-dlp as `channel_is_verified`
   - No additional cost

### Priority 2: Medium Effort, High Value

1. **Add `topicDetails` part** 🟡 Consider
   - Topic categories for better categorization
   - Cost: +2 quota units per video
   - Benefit: Better content classification

2. **Store thumbnail URLs** 🟡 Consider
   - Best thumbnail for preview/analysis
   - No additional API cost (already in response)
   - Benefit: Visual preview capability

3. **Add video bitrate and quality metrics** 🟡 Consider
   - Available in yt-dlp format details
   - No additional cost
   - Benefit: Quality analysis

### Priority 3: Future Enhancements

1. **Visual content analysis** (Requires GPU processing)
   - Scene detection
   - Object recognition
   - Text extraction from video frames

2. **Audio analysis** (Requires audio processing libraries)
   - Music detection
   - Speech-to-text beyond subtitles
   - Audio quality metrics

3. **Advanced NLP** (Requires ML models)
   - Sentiment analysis
   - Topic modeling
   - Clickbait detection

## Implementation Impact

### Collection Capacity (yt-dlp)

**yt-dlp collection method:**
- **No quota limits**: Unlimited videos per day
- **Comprehensive data**: 40+ fields per video
- **Multiple methods**: Channel, trending, keyword scraping
- **All features**: Subtitles, quality metrics, analytics

**Recommendation**: Use yt-dlp for all data collection needs.

### Storage Considerations

Current `score_dictionary` size: ~2-5 KB per idea
With all recommended additions: ~3-8 KB per idea

For 100,000 ideas:
- Current: ~200-500 MB
- With additions: ~300-800 MB
- Still very manageable for SQLite

## Conclusion

**What we're collecting now:**
- ✅ Core engagement metrics (views, likes, comments)
- ✅ Basic content metadata (title, description, tags)
- ✅ Enhanced metrics via yt-dlp (subtitles, quality, engagement rates)
- ✅ Channel information
- ✅ Calculated analytics

**What we can easily add:**
- 🟢 Video quality flags (HD/SD, captions, embeddable)
- 🟢 Privacy and status information
- 🟢 Hashtag extraction
- 🟢 Channel verification status
- 🟢 Topic categories
- 🟢 Thumbnail URLs
- 🟢 Bitrate and format details

**What's possible with more effort:**
- 🟡 Visual content analysis (GPU-based)
- 🟡 Audio analysis
- 🟡 Advanced NLP and sentiment analysis
- 🟡 Predictive trending algorithms

**What's not accessible:**
- ❌ Detailed channel analytics (requires ownership)
- ❌ Real-time recommendation scores
- ❌ User-specific viewing data
- ❌ Accurate dislike counts (hidden by YouTube)

The current implementation is comprehensive for public data. The main opportunities are:
1. Extracting more fields from existing API responses (no extra cost)
2. Mining additional metadata from yt-dlp (already available)
3. Future: GPU-accelerated content analysis
