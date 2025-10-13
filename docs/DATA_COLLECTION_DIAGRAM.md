# Data Collection Flow Diagram

## Current Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         YouTube Shorts                               │
│                    (3-minute vertical videos)                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                │ Collection Methods
                                │
                ┌───────────────┴──────────────┐
                │                              │
                ▼                              ▼
    ┌──────────────────────┐       ┌──────────────────────┐
    │   YouTube API v3     │       │      yt-dlp          │
    │    (Legacy)          │       │   (Recommended)      │
    └──────────┬───────────┘       └──────────┬───────────┘
               │                              │
               │ 15 fields                    │ 40+ fields
               │ 10K quota/day                │ No quota limits
               │                              │
               ▼                              ▼
    ┌──────────────────────────────────────────────────────┐
    │            UniversalMetrics Schema                    │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  Core Engagement (10 fields)                   │  │
    │  │  • view_count, like_count, comment_count       │  │
    │  │  • engagement_rate, like_to_view_ratio         │  │
    │  ├────────────────────────────────────────────────┤  │
    │  │  Content Metadata (12 fields)                  │  │
    │  │  • title, description, tags, subtitles         │  │
    │  │  • duration, hashtags                          │  │
    │  ├────────────────────────────────────────────────┤  │
    │  │  Quality Metrics (8 fields)                    │  │
    │  │  • resolution, fps, aspect_ratio               │  │
    │  │  • has_subtitles, vcodec, acodec               │  │
    │  ├────────────────────────────────────────────────┤  │
    │  │  Channel Info (5 fields)                       │  │
    │  │  • channel_id, channel_title                   │  │
    │  │  • author_follower_count, verified             │  │
    │  ├────────────────────────────────────────────────┤  │
    │  │  Platform Data (5+ fields)                     │  │
    │  │  • upload_date, categories                     │  │
    │  │  • platform_specific (raw data)                │  │
    │  └────────────────────────────────────────────────┘  │
    └──────────────────┬───────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │  SQLite Database        │
         │  ┌───────────────────┐  │
         │  │ ideas table       │  │
         │  │ • source          │  │
         │  │ • source_id       │  │
         │  │ • title           │  │
         │  │ • description     │  │
         │  │ • tags            │  │
         │  │ • score           │  │
         │  │ • score_dictionary│  │
         │  │ • timestamps      │  │
         │  └───────────────────┘  │
         └─────────────────────────┘
```

## Data Collection Breakdown

### What We Collect Now (40+ Fields)

```
┌─────────────────────────────────────────────────────────────┐
│  ENGAGEMENT METRICS (25% of data)                           │
├─────────────────────────────────────────────────────────────┤
│  Raw Counts:                                                │
│  ✅ view_count          ✅ like_count                        │
│  ✅ comment_count       ✅ favorite_count                    │
│  ✅ dislike_count       ❌ share_count (not available)      │
│                                                             │
│  Calculated Ratios:                                         │
│  ✅ engagement_rate        (likes+comments)/views * 100     │
│  ✅ like_to_view_ratio     likes/views * 100                │
│  ✅ comment_to_view_ratio  comments/views * 100             │
│  ✅ views_per_day          average daily views              │
│  ✅ views_per_hour         average hourly views             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CONTENT METADATA (30% of data)                             │
├─────────────────────────────────────────────────────────────┤
│  Text Content:                                              │
│  ✅ title                  ✅ description                    │
│  ✅ tags                   ✅ subtitles (yt-dlp)            │
│  ✅ title_length           ✅ description_length            │
│  ✅ tag_count              🟢 hashtags (easy to add)        │
│                                                             │
│  Video Properties:                                          │
│  ✅ duration_seconds       ✅ resolution (yt-dlp)           │
│  ✅ fps (yt-dlp)           ✅ aspect_ratio (yt-dlp)         │
│  ✅ has_subtitles (yt-dlp) 🟢 definition (hd/sd)           │
│  🟢 caption (boolean)      🟢 dimension (2d/3d)            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CHANNEL/AUTHOR INFO (15% of data)                          │
├─────────────────────────────────────────────────────────────┤
│  ✅ channel_id                ✅ channel_title              │
│  ✅ author_follower_count     🟢 channel_is_verified        │
│  🟢 uploader_id (@handle)     🟢 uploader_url              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PUBLISHING & PLATFORM (15% of data)                        │
├─────────────────────────────────────────────────────────────┤
│  ✅ upload_date (publishedAt) ✅ days_since_upload          │
│  ✅ categories                ✅ platform ("youtube")        │
│  ✅ content_type              🟢 privacy_status             │
│  🟢 embeddable                🟢 made_for_kids              │
│  🟢 license type              🟡 topic_categories          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TECHNICAL DETAILS (15% of data)                            │
├─────────────────────────────────────────────────────────────┤
│  Format Info (yt-dlp):                                      │
│  🟢 vcodec (video codec)      🟢 acodec (audio codec)       │
│  🟢 vbr (video bitrate)       🟢 abr (audio bitrate)        │
│  🟢 tbr (total bitrate)       🟢 filesize                   │
│  🟢 format_id                 🟢 thumbnail_url              │
└─────────────────────────────────────────────────────────────┘
```

## Easy Additions (Priority Matrix)

```
High Value │  ┌─────────────┐  ┌─────────────┐
    ▲      │  │ Definition  │  │ Hashtags    │
    │      │  │ (HD/SD)     │  │ Extraction  │
    │      │  └─────────────┘  └─────────────┘
    │      │  
    │      │  ┌─────────────┐  ┌─────────────┐
    │      │  │ Channel     │  │ Status Info │
    │      │  │ Verified    │  │ (+2 quota)  │
    │      │  └─────────────┘  └─────────────┘
    │      │  
Low Value  │  ┌─────────────┐  ┌─────────────┐
    │      │  │ Bitrate     │  │ Recording   │
    │      │  │ Details     │  │ Location    │
    │      │  └─────────────┘  └─────────────┘
    └──────┴───────────────────────────────────▶
         Low Effort      High Effort

Legend:
• Top-Left: Quick wins (implement first)
• Top-Right: High value but needs work
• Bottom: Nice to have
```

## Future Possibilities (GPU/ML Processing)

```
┌─────────────────────────────────────────────────────────────┐
│  FUTURE: GPU-ACCELERATED ANALYSIS (RTX 5090)                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────────────┐
    │  Visual Content Analysis                             │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  🟡 Face detection (count, positions)          │  │
    │  │  🟡 Scene changes (cuts, transitions)          │  │
    │  │  🟡 Text extraction (OCR on-screen text)       │  │
    │  │  🟡 Object recognition (YOLO/similar)          │  │
    │  │  🟡 Color analysis (dominant colors, palette)  │  │
    │  │  🟡 Aesthetic scoring (ML model)               │  │
    │  └────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────────────┐
    │  Audio Analysis                                      │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  🟡 Music detection & genre classification     │  │
    │  │  🟡 Speech clarity & quality                   │  │
    │  │  🟡 Background noise analysis                  │  │
    │  │  🟡 Audio quality score                        │  │
    │  │  🟡 Tempo/BPM detection                        │  │
    │  └────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────────────┐
    │  Natural Language Processing                         │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  🟡 Sentiment analysis (positive/negative)     │  │
    │  │  🟡 Readability scoring                        │  │
    │  │  🟡 Topic modeling & classification            │  │
    │  │  🟡 Entity extraction (people, places, brands) │  │
    │  │  🟡 Clickbait detection                        │  │
    │  │  🟡 Urgency indicators                         │  │
    │  └────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────────────┐
    │  Trend Prediction                                    │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  🟡 Viral probability score                    │  │
    │  │  🟡 Growth rate prediction                     │  │
    │  │  🟡 Competition analysis                       │  │
    │  │  🟡 Peak views estimation                      │  │
    │  │  🟡 Trend category classification              │  │
    │  └────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────┘
```

## Data Not Accessible

```
┌─────────────────────────────────────────────────────────────┐
│  REQUIRES CHANNEL OWNERSHIP ❌                               │
├─────────────────────────────────────────────────────────────┤
│  Analytics:                                                 │
│  • Watch time                  • Audience retention         │
│  • Average view duration       • Impressions                │
│  • Click-through rate (CTR)    • Traffic sources           │
│  • Demographics (age, gender)  • Geography                  │
│  • Revenue data                • Subscribers gained         │
│  • Cards/End screen clicks     • Playlist metrics           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  REMOVED BY YOUTUBE ❌                                       │
├─────────────────────────────────────────────────────────────┤
│  • Accurate dislike counts (hidden since Dec 2021)          │
│  • Detailed rating breakdowns (removed)                     │
│  • Average rating (deprecated)                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TECHNICAL LIMITATIONS ❌                                    │
├─────────────────────────────────────────────────────────────┤
│  • Real-time view velocity                                  │
│  • Current trending position                                │
│  • Recommendation algorithm scores                          │
│  • User-specific view history                               │
│  • Why video was recommended                                │
└─────────────────────────────────────────────────────────────┘
```

## Comparison: API vs yt-dlp

```
┌──────────────────────────────────────────────────────────────────┐
│                   YouTube Data API v3                            │
├──────────────────────────────────────────────────────────────────┤
│  Provides:                      │  Missing:                      │
│  ✓ Title, description, tags    │  ✗ Subtitles (text)            │
│  ✓ Views, likes, comments      │  ✗ Quality metrics (res/FPS)   │
│  ✓ Channel info, upload date   │  ✗ Enhanced analytics          │
│  ✓ Official & stable           │  ✗ 10,000 units/day limit      │
│  ✓ Fast & reliable             │                                │
├──────────────────────────────────────────────────────────────────┤
│  Best for: Backward compatibility, specific queries              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                          yt-dlp ⭐                                │
├──────────────────────────────────────────────────────────────────┤
│  Provides ALL API fields PLUS: │  Cons:                         │
│  ✓ Title, description, tags    │  ✗ Slower (downloads metadata) │
│  ✓ Views, likes, comments      │  ✗ Unofficial (relies on web)  │
│  ✓ Channel info, upload date   │  ✗ May break with YouTube      │
│  ✓ Subtitles (full text)       │     updates                    │
│  ✓ Quality (resolution, FPS)   │                                │
│  ✓ No quota limits             │                                │
│  ✓ Enhanced analytics          │                                │
├──────────────────────────────────────────────────────────────────┤
│  Best for: Bulk collection, comprehensive analysis, trending     │
└──────────────────────────────────────────────────────────────────┘

Recommendation: Use yt-dlp for all new data collection
```

## Implementation Roadmap

```
Phase 1: Quick Wins (Week 1)
┌──────────────────────────────────────────────────────┐
│  1. Add contentDetails flags (no extra cost)         │
│     □ definition (HD/SD)                             │
│     □ caption (boolean)                              │
│     □ dimension (2d/3d)                              │
│                                                      │
│  2. Extract from yt-dlp (already available)          │
│     □ hashtags                                       │
│     □ channel_is_verified                            │
│     □ thumbnail URLs                                 │
└──────────────────────────────────────────────────────┘

Phase 2: Status Info (Week 2)
┌──────────────────────────────────────────────────────┐
│  1. Add status API part (+2 quota per video)         │
│     □ privacy_status                                 │
│     □ embeddable                                     │
│     □ made_for_kids                                  │
│     □ license type                                   │
│                                                      │
│  2. Add format details from yt-dlp                   │
│     □ video/audio codecs                             │
│     □ bitrates                                       │
│     □ language                                       │
└──────────────────────────────────────────────────────┘

Phase 3: Enhanced Metadata (Week 3-4)
┌──────────────────────────────────────────────────────┐
│  1. Add topicDetails (+2 quota per video)            │
│     □ topic categories                               │
│     □ topic IDs                                      │
│                                                      │
│  2. Add music metadata from yt-dlp                   │
│     □ track, artist, album                           │
└──────────────────────────────────────────────────────┘

Phase 4: Future (Months)
┌──────────────────────────────────────────────────────┐
│  1. GPU-accelerated visual analysis                  │
│  2. Audio content analysis                           │
│  3. NLP sentiment & topic detection                  │
│  4. ML-based trend prediction                        │
└──────────────────────────────────────────────────────┘
```

---

**For detailed information, see:**
- [DATA_COLLECTION_ANALYSIS.md](DATA_COLLECTION_ANALYSIS.md) - Comprehensive analysis
- [DATA_COLLECTION_SUMMARY.md](DATA_COLLECTION_SUMMARY.md) - Quick reference
- [DATA_FIELDS_REFERENCE.md](DATA_FIELDS_REFERENCE.md) - Complete field listing
- [METRICS.md](METRICS.md) - Current metrics documentation
