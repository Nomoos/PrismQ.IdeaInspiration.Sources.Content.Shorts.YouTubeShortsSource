# Complete Data Fields Reference

This document provides a comprehensive reference of all data fields available for YouTube Shorts collection.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Currently collected |
| 🟢 | Easy to add (already in response or low cost) |
| 🟡 | Possible to add (requires extra API call or processing) |
| 🔴 | Not available or not recommended |
| ❌ | Not accessible (requires ownership or removed by YouTube) |

## Data Fields Comparison

### Engagement Metrics

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `view_count` | ✅ Yes | ✅ Yes | ✅ Collected | Core metric |
| `like_count` | ✅ Yes | ✅ Yes | ✅ Collected | Core metric |
| `comment_count` | ✅ Yes | ✅ Yes | ✅ Collected | Core metric |
| `share_count` | ❌ No | ❌ No | ❌ Not Available | Not exposed by YouTube |
| `dislike_count` | ❌ Hidden | ❌ Hidden | ✅ Collected (often null) | Hidden since 2021 |
| `favorite_count` | ✅ Yes | ✅ Yes | ✅ Collected | Usually 0 for Shorts |
| `engagement_rate` | - | - | ✅ Calculated | (likes+comments)/views*100 |
| `like_to_view_ratio` | - | - | ✅ Calculated | likes/views*100 |
| `comment_to_view_ratio` | - | - | ✅ Calculated | comments/views*100 |
| `views_per_day` | - | ✅ Yes | ✅ Calculated | Average daily views |
| `views_per_hour` | - | ✅ Yes | ✅ Calculated | Average hourly views |

### Content Metadata

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `title` | ✅ Yes | ✅ Yes | ✅ Collected | Video title |
| `description` | ✅ Yes | ✅ Yes | ✅ Collected | Full description |
| `tags` | ✅ Yes | ✅ Yes | ✅ Collected | Creator tags |
| `hashtags` | ❌ No | ✅ Yes | 🟢 Easy to add | Extracted from title/desc |
| `duration` | ✅ Yes | ✅ Yes | ✅ Collected | ISO 8601 format |
| `duration_seconds` | - | ✅ Yes | ✅ Collected | Parsed to seconds |
| `title_length` | - | - | ✅ Calculated | Character count |
| `description_length` | - | - | ✅ Calculated | Character count |
| `tag_count` | - | - | ✅ Calculated | Number of tags |
| `categoryId` | ✅ Yes | ✅ Yes | ✅ Collected | YouTube category ID |

### Video Quality

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `resolution` | ❌ No | ✅ Yes | ✅ Collected | e.g., "1080x1920" |
| `fps` | ❌ No | ✅ Yes | ✅ Collected | Frames per second |
| `aspect_ratio` | ❌ No | ✅ Yes | ✅ Collected | e.g., "9:16" |
| `definition` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | "hd" or "sd" |
| `dimension` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | "2d" or "3d" |
| `caption` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | Has captions (boolean) |
| `has_subtitles` | ❌ No | ✅ Yes | ✅ Collected | Boolean |
| `subtitles` | ❌ No | ✅ Yes | ✅ Collected | Full subtitle text |
| `vcodec` | ❌ No | ✅ Yes | 🟢 Easy to add | Video codec |
| `acodec` | ❌ No | ✅ Yes | 🟢 Easy to add | Audio codec |
| `vbr` | ❌ No | ✅ Yes | 🟢 Easy to add | Video bitrate (kbps) |
| `abr` | ❌ No | ✅ Yes | 🟢 Easy to add | Audio bitrate (kbps) |
| `tbr` | ❌ No | ✅ Yes | 🟢 Easy to add | Total bitrate (kbps) |
| `filesize` | ❌ No | ✅ Yes | 🟢 Easy to add | File size (bytes) |

### Channel/Author Information

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `channel_id` | ✅ Yes | ✅ Yes | ✅ Collected | Channel ID |
| `channel_title` | ✅ Yes | ✅ Yes | ✅ Collected | Channel name |
| `author_follower_count` | ❌ No | ✅ Yes | ✅ Collected | Subscriber count |
| `channel_is_verified` | ❌ No | ✅ Yes | 🟢 Easy to add | Verification badge |
| `uploader_id` | ❌ No | ✅ Yes | 🟢 Easy to add | Channel handle (@name) |
| `uploader_url` | ❌ No | ✅ Yes | 🟢 Easy to add | Channel URL |

### Publishing & Status

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `publishedAt` | ✅ Yes | ✅ Yes | ✅ Collected | Upload date (ISO 8601) |
| `upload_date` | ❌ No | ✅ Yes | ✅ Collected | YYYYMMDD format |
| `timestamp` | ❌ No | ✅ Yes | 🟢 Easy to add | Unix timestamp |
| `modified_timestamp` | ❌ No | ✅ Yes | 🟢 Easy to add | Last modified |
| `release_timestamp` | ❌ No | ✅ Yes | 🟢 Easy to add | Scheduled release |
| `days_since_upload` | - | - | ✅ Calculated | Days old |
| `privacyStatus` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | public/unlisted/private |
| `uploadStatus` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | processed/uploaded |
| `license` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | youtube/creativeCommon |
| `embeddable` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | Can be embedded |
| `publicStatsViewable` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | Stats visible |
| `madeForKids` | 🟢 Yes | ✅ Yes | 🟢 Easy to add | COPPA compliance |
| `age_limit` | ❌ No | ✅ Yes | ✅ Collected | Age restriction |

### Visual Elements

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `thumbnail` | ✅ Yes | ✅ Yes | 🟢 Easy to add | Best thumbnail URL |
| `thumbnails` | ✅ Yes | ✅ Yes | 🟢 Easy to add | All thumbnail sizes |
| `has_chapters` | ❌ No | ✅ Yes | 🟢 Easy to add | Has chapter markers |
| `chapter_count` | ❌ No | ✅ Yes | 🟢 Easy to add | Number of chapters |
| `hasCustomThumbnail` | 🔴 Ownership | ❌ No | 🔴 Not Accessible | Requires ownership |

### Topic & Categorization

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `topicIds` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | Freebase topic IDs |
| `topicCategories` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | Wikipedia URLs |
| `relevantTopicIds` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | Related topics |
| `categories` | ✅ Yes | ✅ Yes | ✅ Collected | Category name |
| `genre` | ❌ No | ✅ Yes | 🟢 Easy to add | Genre classification |

### Location & Recording

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `recordingDate` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | When recorded |
| `location.latitude` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | GPS coordinates |
| `location.longitude` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | GPS coordinates |
| `locationDescription` | 🟡 Yes (+2) | ❌ No | 🟡 Possible | Location name |
| `language` | ❌ No | ✅ Yes | 🟢 Easy to add | Primary language code |

### Audio/Music Metadata

| Field | API Method | yt-dlp Method | Status | Notes |
|-------|------------|---------------|--------|-------|
| `track` | ❌ No | ✅ Yes | 🟢 Easy to add | Music track name |
| `artist` | ❌ No | ✅ Yes | 🟢 Easy to add | Music artist |
| `album` | ❌ No | ✅ Yes | 🟢 Easy to add | Album name |
| `release_date` | ❌ No | ✅ Yes | 🟢 Easy to add | Music release date |
| `creator` | ❌ No | ✅ Yes | 🟢 Easy to add | Content creator |

### Advanced Features (Not Yet Implemented)

| Field | Source | Status | Notes |
|-------|--------|--------|-------|
| `faces_detected` | CV Analysis | 🟡 Future | Requires GPU processing |
| `scene_changes` | CV Analysis | 🟡 Future | Requires GPU processing |
| `text_on_screen` | OCR | 🟡 Future | Requires GPU processing |
| `objects_detected` | CV Analysis | 🟡 Future | Requires GPU processing |
| `dominant_colors` | CV Analysis | 🟡 Future | Requires GPU processing |
| `aesthetic_score` | ML Model | 🟡 Future | Requires trained model |
| `music_detected` | Audio Analysis | 🟡 Future | Requires audio processing |
| `speech_clarity` | Audio Analysis | 🟡 Future | Requires audio processing |
| `background_noise` | Audio Analysis | 🟡 Future | Requires audio processing |
| `sentiment_score` | NLP | 🟡 Future | Requires NLP model |
| `readability_score` | NLP | 🟡 Future | Text analysis |
| `clickbait_score` | ML Model | 🟡 Future | Requires trained model |
| `viral_probability` | ML Model | 🟡 Future | Requires trained model |

### Analytics (Require Channel Ownership)

| Field | Status | Notes |
|-------|--------|-------|
| `watch_time` | ❌ Not Accessible | Requires channel ownership |
| `average_view_duration` | ❌ Not Accessible | Requires channel ownership |
| `audience_retention` | ❌ Not Accessible | Requires channel ownership |
| `impressions` | ❌ Not Accessible | Requires channel ownership |
| `ctr` (Click-through rate) | ❌ Not Accessible | Requires channel ownership |
| `traffic_sources` | ❌ Not Accessible | Requires channel ownership |
| `demographics` | ❌ Not Accessible | Requires channel ownership |
| `revenue` | ❌ Not Accessible | Requires channel ownership |
| `subscribers_gained` | ❌ Not Accessible | Requires channel ownership |
| `cards_clicks` | ❌ Not Accessible | Requires channel ownership |
| `end_screen_clicks` | ❌ Not Accessible | Requires channel ownership |

## Summary Statistics

### Currently Collected
- **Total fields**: 40+ metrics in UniversalMetrics
- **Collection method**: yt-dlp (primary)
- **Core metadata**: Title, description, tags, views, likes, comments, channel info
- **Enhanced data**: Subtitles (full text), quality metrics (resolution, FPS, aspect ratio)
- **Analytics**: Engagement rate, views per day/hour, like-to-view ratios
- **Calculated metrics**: ~10 derived fields

### Easy to Add (High Priority)
- **No extra cost**: ~20 fields (already in yt-dlp responses)
- **Total potential**: 60+ fields via yt-dlp

### Future Possibilities
- **GPU-based analysis**: 20+ additional fields
- **NLP analysis**: 10+ additional fields
- **Audio analysis**: 10+ additional fields

### Not Accessible
- **Ownership required**: 15+ analytics fields
- **Removed by YouTube**: 2-3 fields (dislikes, ratings)
- **Technical limitations**: 5+ fields

## Quick Reference by Collection Method

### Current Implementation (yt-dlp)
```
✅ Core metadata (title, description, tags)
✅ Engagement (views, likes, comments, favorites)
✅ Channel info (ID, name, subscribers, verification)
✅ Publishing info (date, category)
✅ Subtitles (full text extraction)
✅ Quality metrics (resolution, FPS, aspect ratio, codecs)
✅ Analytics (engagement rate, views per day/hour)
🟢 Can add: hashtags, music metadata, additional format details
```

### yt-dlp Collection Methods ⭐
```
Channel Scraping:
  ✅ Comprehensive metadata for specific channels
  ✅ All fields listed above
  ✅ Best for targeted collection

Trending Scraping:
  ✅ Discover viral content
  ✅ Same comprehensive metadata
  ✅ Best for trend analysis

Keyword Scraping:
  ✅ Flexible search by topics
  ✅ Same comprehensive metadata
  ✅ Best for broad collection
```

### Future GPU/ML Processing
```
🟡 Visual content analysis
🟡 Audio quality analysis
🟡 Natural language processing
🟡 Trend prediction
```

## Implementation Priority

### Phase 1: Quick Wins (Week 1)
1. Add `definition`, `caption`, `dimension` from contentDetails
2. Extract `hashtags` from yt-dlp
3. Add `channel_is_verified` from yt-dlp
4. Add `thumbnail` URLs

### Phase 2: Status Information (Week 2)
1. Add `status` API part (+2 quota)
2. Collect privacy, embeddable, madeForKids
3. Add language and format details from yt-dlp

### Phase 3: Enhanced Metadata (Week 3-4)
1. Add `topicDetails` API part (+2 quota)
2. Collect music/audio metadata from yt-dlp
3. Add bitrate and quality metrics

### Phase 4: Future Enhancements (Later)
1. Implement visual content analysis
2. Add audio analysis capabilities
3. Implement NLP features
4. Build trend prediction model

---

**Last Updated**: 2025-10-13  
**Current Version**: 1.0.0
