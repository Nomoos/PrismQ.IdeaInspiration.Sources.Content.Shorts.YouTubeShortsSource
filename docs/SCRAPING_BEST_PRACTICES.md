# YouTube Shorts Scraping Best Practices

## Overview

This document addresses common questions about YouTube Shorts scraping, including:
- How views_per_day is calculated
- Whether to re-scrape videos or download once
- Safety considerations and ban prevention
- Alternative scrapers and downloaders

## How Views Per Day is Calculated

### Current Implementation

The `views_per_day` metric is calculated as follows:

```python
# From src/sources/youtube_channel_plugin.py (lines 297-307)
views_per_day = 0.0
upload_date_str = metadata.get('upload_date')  # Format: YYYYMMDD (e.g., "20231015")

if upload_date_str and view_count > 0:
    upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
    days_since_upload = (datetime.now() - upload_date).days
    
    if days_since_upload > 0:
        views_per_day = view_count / days_since_upload
```

### How It Works

1. **Upload Date**: Extracted from YouTube metadata in YYYYMMDD format
2. **Days Since Upload**: Calculated as `(current_date - upload_date).days`
3. **Views Per Day**: `total_views / days_since_upload`

### Example

```
Video uploaded: October 1, 2023
Current date: October 15, 2023
Days since upload: 14 days
Total views: 100,000
Views per day: 100,000 / 14 = 7,142 views/day
```

### Important Notes

- **Snapshot Metric**: This is a point-in-time calculation based on current view count
- **Average Only**: Represents average performance, not actual daily breakdown
- **No Historical Data**: We don't track how views accumulated over time
- **Recalculated on Re-scrape**: If you re-scrape the same video later, views_per_day will be updated with new data

## Re-Scraping vs. One-Time Download

### Question: Should I Re-Scrape Videos or Download Once?

**Answer: It depends on your use case.**

### Strategy 1: One-Time Collection (Recommended for Most Use Cases) ✅

**When to use:**
- Building an idea inspiration library
- Content research and analysis
- Studying successful formats
- Training data for ML models

**Advantages:**
- ✅ **Safer**: Minimal risk of rate limiting or bans
- ✅ **Faster**: No repeated downloads
- ✅ **Simpler**: Database deduplication handles duplicates automatically
- ✅ **Efficient**: Lower bandwidth and storage usage
- ✅ **Stable**: Snapshot represents video at specific time

**Implementation:**
```bash
# Scrape once and store
python -m src.cli scrape-channel --channel @channelname --top 50

# Data persists in database with UNIQUE(source, source_id)
# Re-running won't create duplicates, will update existing records
```

**Database Behavior:**
```sql
-- From src/database.py
UNIQUE(source, source_id)
ON CONFLICT(source, source_id) DO UPDATE SET
    -- Updates existing records instead of creating duplicates
```

### Strategy 2: Periodic Re-Scraping (For Tracking Growth)

**When to use:**
- Tracking viral video performance
- Monitoring engagement trends over time
- Studying view velocity patterns
- Competitive analysis

**Advantages:**
- ✅ **Updated Data**: Get current view counts and engagement
- ✅ **Trend Analysis**: Track how videos perform over time
- ✅ **Growth Metrics**: Calculate acceleration/deceleration

**Disadvantages:**
- ⚠️ **Higher Risk**: More requests = higher chance of throttling
- ⚠️ **Slower**: Multiple download sessions
- ⚠️ **Complexity**: Need to store historical snapshots
- ⚠️ **Bandwidth**: Repeated downloads use more resources

**Recommended Frequency:**
- **Conservative**: Weekly (every 7 days)
- **Moderate**: Every 3 days
- **Aggressive**: Daily (higher risk)

**Implementation:**
```python
# Pseudo-code for periodic re-scraping
import time
from datetime import datetime, timedelta

def periodic_rescrape(video_id, min_interval_days=7):
    """Re-scrape video if enough time has passed."""
    last_scrape = get_last_scrape_date(video_id)
    
    if not last_scrape or (datetime.now() - last_scrape) > timedelta(days=min_interval_days):
        # Safe to re-scrape
        scrape_video(video_id)
        update_last_scrape_date(video_id, datetime.now())
        
        # Add delay between requests
        time.sleep(5)  # 5 second delay
```

## Ban Prevention and Safety

### Is Re-Scraping Safe?

**Short Answer: Mostly safe with proper precautions, but one-time collection is safer.**

### Risk Factors

| Factor | Risk Level | Mitigation |
|--------|-----------|------------|
| **Frequency** | 🟡 Medium | Limit to weekly or less frequent |
| **Volume** | 🟡 Medium | Max 100-200 videos per session |
| **Speed** | 🔴 High | Always add delays (5-10s between requests) |
| **Pattern** | 🟡 Medium | Vary timing, don't scrape at exact intervals |
| **IP Address** | 🟢 Low | Use residential IP, avoid datacenter IPs |

### YouTube's Position on Scraping

**Official Stance:**
- YouTube Terms of Service (Section 4.B): "You are not allowed to... access the Service using any automated means (such as robots, botnets or scrapers)"
- However, yt-dlp is widely used and tolerated for personal use
- YouTube primarily targets commercial-scale scraping operations

**Reality:**
- ✅ **Personal Use**: Generally tolerated
- ⚠️ **Research Use**: Gray area, proceed with caution
- ❌ **Commercial Use**: High risk of legal action

### Best Practices for Safe Scraping

#### 1. Use yt-dlp (Not YouTube API for Heavy Scraping)

**Why yt-dlp is safer:**
- No API quota (so no "hard limit" violations)
- Uses same endpoints as regular YouTube viewing
- Mimics browser behavior
- Regularly updated to adapt to YouTube changes

**YouTube API Risks:**
- Hard quota limits (10,000 units/day)
- Easier to track and throttle
- Requires registration (traceable)

#### 2. Implement Rate Limiting

```python
import time
import random

def scrape_with_delays(video_ids):
    for video_id in video_ids:
        scrape_video(video_id)
        
        # Random delay between 5-15 seconds
        delay = random.uniform(5, 15)
        print(f"Waiting {delay:.1f}s before next request...")
        time.sleep(delay)
```

#### 3. Respect YouTube's Infrastructure

```python
# Good practices:
- Limit concurrent connections (don't parallelize too much)
- Scrape during off-peak hours (avoid 12pm-3pm UTC)
- Use realistic user-agent strings
- Don't overwhelm specific channels
```

#### 4. Error Handling and Backoff

```python
import time

def scrape_with_retry(video_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            return scrape_video(video_id)
        except Exception as e:
            if "429" in str(e):  # Rate limited
                wait_time = (2 ** attempt) * 60  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    return None
```

### Signs You're Being Throttled

Watch for these indicators:
- ⚠️ **HTTP 429 errors**: Too Many Requests
- ⚠️ **Slow response times**: Unusual delays
- ⚠️ **Incomplete metadata**: Missing fields in responses
- ⚠️ **CAPTCHA challenges**: Asked to verify you're human

**If throttled:**
1. Stop scraping immediately
2. Wait 24-48 hours
3. Reduce frequency/volume when resuming
4. Implement longer delays

### Recommended Scraping Schedule

#### Conservative (Safest) ⭐ Recommended

```
Initial scrape: Collect all videos once
Re-scrape frequency: Every 14 days (for trend tracking)
Daily limit: 50-100 videos
Delay between requests: 10-15 seconds
Risk level: 🟢 Very Low
```

#### Moderate (Balanced)

```
Initial scrape: Collect all videos once
Re-scrape frequency: Every 7 days
Daily limit: 100-200 videos
Delay between requests: 5-10 seconds
Risk level: 🟡 Low-Medium
```

#### Aggressive (Higher Risk)

```
Initial scrape: Collect all videos once
Re-scrape frequency: Every 3 days
Daily limit: 200-300 videos
Delay between requests: 3-5 seconds
Risk level: 🔴 Medium-High
```

## Alternative Scrapers and Downloaders

### Current: yt-dlp (Recommended) ⭐

**Pros:**
- ✅ Actively maintained (weekly updates)
- ✅ Comprehensive metadata extraction
- ✅ Handles YouTube changes quickly
- ✅ Large community (1M+ GitHub stars)
- ✅ Subtitle support
- ✅ Quality metrics (resolution, FPS)

**Cons:**
- ⚠️ Can break when YouTube updates
- ⚠️ Requires Python installation
- ⚠️ Slower than API for bulk collection

**Repository:** https://github.com/yt-dlp/yt-dlp

### Alternative 1: youtube-dl (Not Recommended)

**Status:** ⚠️ Legacy, less actively maintained

**Pros:**
- ✅ Mature codebase
- ✅ Similar API to yt-dlp

**Cons:**
- ❌ Slower update cycle
- ❌ Often broken during YouTube updates
- ❌ yt-dlp is a better-maintained fork

**Recommendation:** Use yt-dlp instead

### Alternative 2: YouTube Data API v3

**Status:** ✅ Official, stable

**What it provides:**
- ✅ Title, description, tags
- ✅ Views, likes, comments, favorites
- ✅ Channel info, upload date, categories

**What it's missing:**
- ❌ Subtitles (no text extraction)
- ❌ Quality metrics (no resolution, FPS, aspect ratio)
- ❌ Enhanced analytics (calculated metrics)

**Pros:**
- ✅ Official Google API
- ✅ Guaranteed stability
- ✅ Fast for small queries
- ✅ Well-documented

**Cons:**
- ❌ Quota limits (10,000 units/day)
- ❌ No subtitles or quality metrics
- ❌ No trending access

**When to use:**
- Small-scale queries (<1,000 videos)
- Need guaranteed uptime
- Official data requirements
- Don't need subtitles or quality metrics

### Alternative 3: Invidious API

**Status:** 🟡 Community-run, variable reliability

**What it is:** Privacy-focused YouTube frontend with API

**Pros:**
- ✅ No Google account needed
- ✅ JSON API
- ✅ No quotas

**Cons:**
- ❌ Dependent on instance availability
- ❌ Inconsistent uptime
- ❌ May lack latest features
- ❌ Legal gray area

**Instances:** https://api.invidious.io/

**Example:**
```bash
curl "https://invidious.instance.com/api/v1/videos/VIDEO_ID"
```

### Alternative 4: pytube (Not Recommended for Scraping)

**Status:** ⚠️ Focused on downloads, not metadata

**Pros:**
- ✅ Pure Python
- ✅ Good for downloading videos

**Cons:**
- ❌ Limited metadata extraction
- ❌ Less maintained than yt-dlp
- ❌ Frequently broken

**Recommendation:** Use yt-dlp instead

### Alternative 5: YouTube RSS Feeds

**Status:** ✅ Lightweight, safe for monitoring

**What it is:** YouTube's official RSS feeds for channels

**Pros:**
- ✅ Official and stable
- ✅ Very lightweight
- ✅ No scraping concerns
- ✅ Real-time updates

**Cons:**
- ❌ Limited metadata (title, description, thumbnail only)
- ❌ No view counts or engagement data
- ❌ No quality metrics

**URL Format:**
```
https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
```

**When to use:**
- Monitoring new uploads
- Building watch lists
- Feed aggregation

### Comparison Table

| Tool | Metadata | Speed | Stability | Quotas | Risk | Recommendation |
|------|----------|-------|-----------|--------|------|----------------|
| **yt-dlp** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ∞ | 🟢 Low | ✅ Best choice |
| **YouTube API** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 10K/day | 🟢 None | Small queries |
| **youtube-dl** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ∞ | 🟢 Low | ❌ Use yt-dlp |
| **Invidious** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ∞ | 🟡 Medium | Experimental |
| **pytube** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ∞ | 🟢 Low | ❌ Use yt-dlp |
| **RSS Feeds** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ∞ | 🟢 None | Monitoring only |

## Recommendations Summary

### For Idea Collection (Most Users) ⭐

**Strategy:**
1. Use yt-dlp (current implementation)
2. Download videos once
3. Store in database (automatic deduplication)
4. No re-scraping needed

**Why:**
- Safest approach
- Meets 95% of use cases
- Simple to implement
- Low risk

### For Trend Tracking (Advanced Users)

**Strategy:**
1. Use yt-dlp (current implementation)
2. Initial scrape: Collect all videos
3. Re-scrape: Weekly (14 days for safety)
4. Implement delays: 10-15 seconds between requests
5. Daily limit: 50-100 videos maximum

**Implementation checklist:**
- [ ] Add delay between requests (10-15s)
- [ ] Track last scrape date for each video
- [ ] Implement exponential backoff on errors
- [ ] Monitor for throttling indicators
- [ ] Store historical snapshots in separate table

### Best Practices Checklist

- [ ] Use yt-dlp as primary scraper
- [ ] Implement random delays (5-15s) between requests
- [ ] Limit daily volume (50-200 videos max)
- [ ] Add exponential backoff on errors
- [ ] Monitor for HTTP 429 errors
- [ ] Scrape during off-peak hours
- [ ] Use realistic user-agent strings
- [ ] Store last scrape timestamp
- [ ] Implement database deduplication
- [ ] Log all scraping activities

## Code Examples

### Safe Re-Scraping Implementation

```python
import time
import random
from datetime import datetime, timedelta
from src.database import Database
from src.sources.youtube_channel_plugin import YouTubeChannelPlugin

def safe_rescrape(video_ids, min_interval_days=14, delay_range=(10, 15)):
    """Safely re-scrape videos with rate limiting.
    
    Args:
        video_ids: List of video IDs to re-scrape
        min_interval_days: Minimum days between re-scrapes (default: 14)
        delay_range: (min, max) delay in seconds between requests
    """
    db = Database('ideas.db')
    
    for i, video_id in enumerate(video_ids, 1):
        # Check last scrape date
        idea = db.get_idea('youtube_channel', video_id)
        
        if idea:
            last_update = datetime.fromisoformat(idea['updated_at'])
            days_since = (datetime.now() - last_update).days
            
            if days_since < min_interval_days:
                print(f"[{i}/{len(video_ids)}] Skipping {video_id}: Last scraped {days_since} days ago")
                continue
        
        # Scrape with delay
        print(f"[{i}/{len(video_ids)}] Re-scraping {video_id}...")
        try:
            # Your scraping logic here
            metadata = scrape_video(video_id)
            
            if metadata:
                # Update database
                db.insert_idea(...)  # Updates existing record
                print(f"  ✓ Updated successfully")
            
            # Random delay between requests
            delay = random.uniform(*delay_range)
            print(f"  Waiting {delay:.1f}s before next request...")
            time.sleep(delay)
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            if "429" in str(e):
                print("  ⚠️ Rate limited! Stopping...")
                break
    
    db.close()
```

### Tracking Historical Data

```python
# Extend database schema to track history
def create_history_table():
    """Create table for historical snapshots."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS idea_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            source_id TEXT NOT NULL,
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER,
            views_per_day REAL,
            engagement_rate REAL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(source, source_id) REFERENCES ideas(source, source_id)
        )
    """)

def save_snapshot(source, source_id, metrics):
    """Save historical snapshot of metrics."""
    cursor.execute("""
        INSERT INTO idea_history 
        (source, source_id, view_count, like_count, comment_count, 
         views_per_day, engagement_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (source, source_id, metrics.view_count, metrics.like_count,
          metrics.comment_count, metrics.views_per_day, metrics.engagement_rate))
```

## Conclusion

**Key Takeaways:**

1. **views_per_day** is calculated by dividing total views by days since upload
2. **One-time collection** is recommended for most use cases (safer, simpler)
3. **Re-scraping** should be done weekly at most, with 10-15s delays
4. **yt-dlp** is the best tool (already implemented)
5. **Safety first**: Implement delays, monitor for throttling, respect YouTube's infrastructure

**Next Steps:**

1. Use current implementation (yt-dlp) for one-time collection
2. Only implement re-scraping if you need trend tracking
3. If re-scraping, follow the "Conservative" schedule (weekly, 50-100 videos/day)
4. Monitor for any throttling indicators
5. Consider creating a separate table for historical snapshots if tracking trends

---

**Last Updated:** 2025-10-13  
**Related Documentation:**
- [DATA_COLLECTION_ANALYSIS.md](DATA_COLLECTION_ANALYSIS.md) - What data we collect
- [METRICS.md](METRICS.md) - Metrics documentation
- [README.md](../README.md) - Main project documentation
