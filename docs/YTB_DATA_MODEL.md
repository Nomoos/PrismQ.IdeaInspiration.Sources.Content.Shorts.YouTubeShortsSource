# YouTube Data Model for SQLite Database (S3DB) Storage

## Overview

This document describes the data model used to store YouTube Shorts inspiration data in the SQLite database (S3DB). The system uses SQLAlchemy ORM for type-safe database operations and maintains two table structures for backward compatibility.

## Table of Contents

- [Database Schema](#database-schema)
- [Data Model Architecture](#data-model-architecture)
- [Field Descriptions](#field-descriptions)
- [Data Flow](#data-flow)
- [Storage Format](#storage-format)
- [Query Patterns](#query-patterns)
- [Examples](#examples)
- [Performance Considerations](#performance-considerations)

## Database Schema

### Primary Table: `youtube_shorts_source`

The main table for storing YouTube Shorts data using SQLAlchemy ORM:

```sql
CREATE TABLE youtube_shorts_source (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source VARCHAR(100) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    score FLOAT,
    score_dictionary TEXT,
    processed BOOLEAN DEFAULT 0 NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Indexes for performance
CREATE UNIQUE INDEX ix_source_source_id ON youtube_shorts_source (source, source_id);
CREATE INDEX ix_score ON youtube_shorts_source (score);
CREATE INDEX ix_youtube_shorts_source_source ON youtube_shorts_source (source);
CREATE INDEX ix_created_at ON youtube_shorts_source (created_at);
CREATE INDEX ix_youtube_shorts_source_source_id ON youtube_shorts_source (source_id);
CREATE INDEX ix_processed ON youtube_shorts_source (processed);
```

### Legacy Table: `ideas`

Maintained for backward compatibility:

```sql
CREATE TABLE ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    score REAL,
    score_dictionary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, source_id)
);
```

## Data Model Architecture

### ORM Model Class

Located in `mod/Model/youtube_shorts_source.py`:

```python
class YouTubeShortsSource(Base):
    """Model for storing YouTube Shorts idea inspirations."""
    
    __tablename__ = 'youtube_shorts_source'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Source information
    source = Column(String(100), nullable=False, index=True)
    source_id = Column(String(255), nullable=False, index=True)
    
    # Content fields
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    
    # Scoring
    score = Column(Float, nullable=True)
    score_dictionary = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
```

### Database Context

Located in `mod/Model/db_context.py`:

```python
class DBContext:
    """Database context for managing YouTube Shorts data with CRUD operations."""
    
    def __init__(self, db_path: str = "ideas.db"):
        """Initialize database context."""
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._init_db()
```

## Field Descriptions

### Core Fields

| Field | Type | Nullable | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | INTEGER | No | Auto-incrementing primary key | `1`, `2`, `3` |
| `source` | VARCHAR(100) | No | Platform identifier | `youtube`, `youtube_channel`, `youtube_trending` |
| `source_id` | VARCHAR(255) | No | Unique video ID from YouTube | `dQw4w9WgXcQ` |
| `title` | TEXT | No | Video title | `"Amazing Startup Ideas 2025"` |
| `description` | TEXT | Yes | Video description/transcript | Full video description text |
| `tags` | TEXT | Yes | Comma-separated tags | `youtube_shorts,business,ideas` |
| `score` | FLOAT | Yes | Calculated idea score | `85.5`, `92.3` |
| `score_dictionary` | TEXT | Yes | JSON string of metrics | See [Score Dictionary Format](#score-dictionary-format) |
| `processed` | BOOLEAN | No | Processing status flag (default: False) | `0` (False), `1` (True) |
| `created_at` | DATETIME | No | Record creation timestamp (UTC) | `2025-01-15T10:30:00+00:00` |
| `updated_at` | DATETIME | No | Last update timestamp (UTC) | `2025-01-15T12:45:00+00:00` |

### Field Constraints

- **Unique Constraint**: `(source, source_id)` - Prevents duplicate entries for the same video
- **Indexes**: Optimized for queries on `source`, `source_id`, `score`, `processed`, and `created_at`
- **Validation**: `score_dictionary` must be valid JSON when set
- **Processing Status**: `processed` field defaults to `False` on creation and is set to `True` by the builder after transformation

## Data Flow

### 1. Scraping → Model Conversion

```
YouTube API/yt-dlp → Plugin scrape() → metrics dict → YouTubeShortsSource ORM
```

**Step-by-step:**

1. **Scraping Plugin** (e.g., `YouTubeChannelPlugin`) fetches video metadata
2. **Metadata Extraction** converts raw data to standardized metrics format
3. **Universal Metrics** factory creates normalized metrics dictionary
4. **ORM Model** converts metrics to database fields
5. **Database Context** persists data with CRUD operations

### 2. Data Transformation Pipeline

```python
# Raw yt-dlp metadata
metadata = {
    'id': 'dQw4w9WgXcQ',
    'title': 'Amazing Video',
    'view_count': 1000000,
    'like_count': 50000,
    # ... more fields
}

# Convert to idea format
idea = {
    'source_id': 'dQw4w9WgXcQ',
    'title': 'Amazing Video',
    'description': '...',
    'tags': 'youtube_shorts,viral',
    'metrics': {
        'snippet': {...},
        'statistics': {...},
        'enhanced_metrics': {...}
    }
}

# Store in database via DBContext
db.upsert(
    source='youtube_channel',
    source_id='dQw4w9WgXcQ',
    title='Amazing Video',
    description='...',
    tags='youtube_shorts,viral',
    score=85.5,
    score_dictionary=json.dumps(metrics)
)
```

## Storage Format

### Score Dictionary Format

The `score_dictionary` field stores a JSON string with comprehensive video metrics:

```json
{
  "id": "dQw4w9WgXcQ",
  "snippet": {
    "title": "Amazing Startup Ideas 2025",
    "description": "Check out these amazing startup ideas...",
    "publishedAt": "20250115",
    "channelId": "UCxxxxxxxxxxxxxxxx",
    "channelTitle": "Tech Insights",
    "categoryId": "28",
    "tags": ["startup", "business", "ideas"]
  },
  "statistics": {
    "viewCount": "1000000",
    "likeCount": "50000",
    "commentCount": "2500",
    "favoriteCount": "0"
  },
  "contentDetails": {
    "duration": "PT2M30S"
  },
  "enhanced_metrics": {
    "engagement_rate": 5.25,
    "views_per_day": 12500.0,
    "resolution": "1080x1920",
    "fps": 30,
    "aspect_ratio": "1080:1920",
    "subtitle_text": "Full transcript of video...",
    "subtitles_available": true,
    "channel_follower_count": 500000
  }
}
```

### Tags Format

Tags are stored as comma-separated values:

```
youtube_shorts,channel_short,Tech Insights,category_Science & Technology,startup,business
```

### Timestamp Format

Timestamps use timezone-aware UTC format:

```python
created_at = datetime.now(timezone.utc)  # 2025-01-15T10:30:00+00:00
```

## Query Patterns

### Common Queries

#### 1. Get Top Scored Videos

```python
from mod.Model import DBContext

with DBContext('ideas.db') as db:
    top_videos = db.list_all(limit=10, order_by='score', ascending=False)
    for video in top_videos:
        print(f"{video.title}: {video.score}")
```

#### 2. Find Videos by Source

```python
with DBContext('ideas.db') as db:
    # Get all channel-scraped videos
    channel_videos = [v for v in db.list_all() if v.source == 'youtube_channel']
    
    # Count by source
    count = db.count_by_source('youtube_channel')
```

#### 3. Search by Tags

```python
with DBContext('ideas.db') as db:
    all_videos = db.list_all()
    startup_videos = [v for v in all_videos if 'startup' in v.tags.lower()]
```

#### 4. Get Recent Videos

```python
with DBContext('ideas.db') as db:
    recent = db.list_all(limit=20, order_by='created_at', ascending=False)
```

#### 5. Check for Duplicates

```python
with DBContext('ideas.db') as db:
    existing = db.read('youtube_channel', 'dQw4w9WgXcQ')
    if existing:
        print(f"Video already exists: {existing.title}")
```

### Raw SQL Queries

For advanced queries, use SQLAlchemy session:

```python
from mod.Model import DBContext
from mod.Model.youtube_shorts_source import YouTubeShortsSource

with DBContext('ideas.db') as db:
    with db.get_session() as session:
        # Complex query with multiple conditions
        videos = session.query(YouTubeShortsSource)\
            .filter(YouTubeShortsSource.score > 80)\
            .filter(YouTubeShortsSource.source == 'youtube_channel')\
            .order_by(YouTubeShortsSource.created_at.desc())\
            .limit(10)\
            .all()
```

## Examples

### Example 1: Creating a Record

```python
from mod.Model import DBContext
import json

# Metrics from scraping
metrics = {
    'snippet': {
        'title': 'Top 10 Startup Ideas',
        'channelTitle': 'Business Hub',
        'tags': ['startup', 'business']
    },
    'statistics': {
        'viewCount': '500000',
        'likeCount': '25000',
        'commentCount': '1200'
    },
    'enhanced_metrics': {
        'engagement_rate': 5.24,
        'views_per_day': 6250.0
    }
}

# Create record
with DBContext('ideas.db') as db:
    record = db.create(
        source='youtube_channel',
        source_id='abc123xyz',
        title='Top 10 Startup Ideas',
        description='Discover the best startup ideas for 2025...',
        tags='youtube_shorts,startup,business',
        score=87.5,
        score_dictionary=metrics
    )
    print(f"Created: {record.id}")
```

### Example 2: Reading and Updating

```python
from mod.Model import DBContext

with DBContext('ideas.db') as db:
    # Read existing record
    video = db.read('youtube_channel', 'abc123xyz')
    
    if video:
        # Get score dictionary
        metrics = video.get_score_dict()
        print(f"Views: {metrics['statistics']['viewCount']}")
        
        # Update score
        db.update(
            source='youtube_channel',
            source_id='abc123xyz',
            score=90.0
        )
```

### Example 3: Upsert Pattern

```python
from mod.Model import DBContext

with DBContext('ideas.db') as db:
    # Upsert - insert if new, update if exists
    video = db.upsert(
        source='youtube_trending',
        source_id='xyz789abc',
        title='Viral Trending Short',
        score=95.0,
        score_dictionary={'statistics': {'viewCount': '2000000'}}
    )
    print(f"Video ID: {video.id}, Score: {video.score}")
```

### Example 4: Exporting Data

```python
from mod.Model import DBContext
import json

with DBContext('ideas.db') as db:
    # Get all videos
    videos = db.list_all(limit=100)
    
    # Convert to list of dicts
    export_data = [video.to_dict() for video in videos]
    
    # Save as JSON
    with open('export.json', 'w') as f:
        json.dump(export_data, f, indent=2)
```

### Example 5: Data Analysis

```python
from mod.Model import DBContext
from collections import Counter

with DBContext('ideas.db') as db:
    videos = db.list_all()
    
    # Analyze by source
    source_counts = Counter(v.source for v in videos)
    print(f"Videos by source: {dict(source_counts)}")
    
    # Average score
    scores = [v.score for v in videos if v.score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"Average score: {avg_score:.2f}")
    
    # Top tags
    all_tags = []
    for v in videos:
        if v.tags:
            all_tags.extend(v.tags.split(','))
    top_tags = Counter(all_tags).most_common(10)
    print(f"Top tags: {top_tags}")
```

## Performance Considerations

### Indexes

The database uses several indexes for optimal query performance:

1. **Unique Index**: `(source, source_id)` - Fast duplicate checking during upsert
2. **Score Index**: Fast sorting and filtering by score
3. **Source Index**: Quick filtering by source type
4. **Source ID Index**: Fast lookups by video ID
5. **Created At Index**: Efficient temporal queries

### Best Practices

1. **Use Context Managers**: Ensures proper connection cleanup
   ```python
   with DBContext('ideas.db') as db:
       # operations here
   ```

2. **Batch Operations**: For multiple inserts, use session context
   ```python
   with db.get_session() as session:
       for idea in ideas:
           record = YouTubeShortsSource(...)
           session.add(record)
       # Commits all at once
   ```

3. **Limit Results**: Use pagination for large datasets
   ```python
   videos = db.list_all(limit=100)
   ```

4. **Index-Friendly Queries**: Filter by indexed columns first
   ```python
   # Good - uses indexes
   db.read('youtube', 'video_id')
   
   # Less efficient - full table scan
   all_videos = db.list_all()
   filtered = [v for v in all_videos if 'keyword' in v.title]
   ```

5. **JSON Field Access**: Parse score_dictionary only when needed
   ```python
   # Lazy parsing
   metrics = video.get_score_dict()
   if metrics:
       views = metrics['statistics']['viewCount']
   ```

### Storage Optimization

- **SQLite Vacuum**: Periodically run `VACUUM` to reclaim space
  ```python
  import sqlite3
  conn = sqlite3.connect('ideas.db')
  conn.execute('VACUUM')
  conn.close()
  ```

- **Index Maintenance**: Indexes are automatically maintained
- **File Size**: Expect ~1-5 KB per record depending on metadata size

## Database Initialization

### Automatic Initialization

The database schema is created automatically:

```python
from mod.Model import DBContext

# Schema created on first instantiation
db = DBContext('ideas.db')
```

### Manual Initialization

Using the init script:

```bash
# Default path
python scripts/init_db.py

# Custom path
python scripts/init_db.py --db-path /path/to/database.db

# With verbose output
python scripts/init_db.py --verbose
```

## Migration and Backup

### Backup Database

```bash
# Simple file copy
cp ideas.db ideas_backup_$(date +%Y%m%d).db

# SQLite backup command
sqlite3 ideas.db ".backup ideas_backup.db"
```

### Export to CSV

```python
import csv
from mod.Model import DBContext

with DBContext('ideas.db') as db:
    videos = db.list_all()
    
    with open('export.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'source', 'source_id', 'title', 'score', 'created_at'
        ])
        writer.writeheader()
        
        for video in videos:
            writer.writerow({
                'id': video.id,
                'source': video.source,
                'source_id': video.source_id,
                'title': video.title,
                'score': video.score,
                'created_at': video.created_at.isoformat()
            })
```

### Import from Legacy Table

```python
import sqlite3
import json
from mod.Model import DBContext

# Connect to legacy database
conn = sqlite3.connect('ideas.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Read from old table
cursor.execute("SELECT * FROM ideas")
old_records = cursor.fetchall()

# Write to new model
db = DBContext('ideas.db')
for record in old_records:
    db.upsert(
        source=record['source'],
        source_id=record['source_id'],
        title=record['title'],
        description=record['description'],
        tags=record['tags'],
        score=record['score'],
        score_dictionary=json.loads(record['score_dictionary']) if record['score_dictionary'] else None
    )

conn.close()
db.close()
print(f"Migrated {len(old_records)} records")
```

## Troubleshooting

### Common Issues

#### 1. IntegrityError: UNIQUE constraint failed

**Cause**: Attempting to insert duplicate (source, source_id)

**Solution**: Use `upsert()` instead of `create()`

```python
# Instead of this
db.create(source='youtube', source_id='abc')

# Use this
db.upsert(source='youtube', source_id='abc')
```

#### 2. Invalid JSON in score_dictionary

**Cause**: Non-JSON string stored in score_dictionary field

**Solution**: Always validate before storing

```python
import json

try:
    json.dumps(metrics)  # Validate
    db.create(..., score_dictionary=metrics)
except TypeError:
    print("Invalid metrics format")
```

#### 3. Database locked

**Cause**: Multiple processes accessing database simultaneously

**Solution**: Use context managers and shorter transactions

```python
# Good - short transaction
with DBContext('ideas.db') as db:
    video = db.read('youtube', 'abc')
# Connection closed

# Bad - long-running connection
db = DBContext('ideas.db')
time.sleep(60)  # Locks database
db.close()
```

## Related Documentation

- [Model Implementation](MODEL_IMPLEMENTATION.md) - ORM implementation details
- [Model Layer README](../mod/Model/README.md) - CRUD operations guide
- [Data Fields Reference](DATA_FIELDS_REFERENCE.md) - Complete field catalog
- [Metrics Documentation](METRICS.md) - Universal metrics system
- [Data Collection Guide](DATA_COLLECTION_GUIDE.md) - What data we collect

## Summary

The YouTube data model for SQLite storage provides:

- **Type-safe operations** via SQLAlchemy ORM
- **Efficient storage** with proper indexing
- **Flexible metrics** via JSON score_dictionary
- **Backward compatibility** with legacy table
- **Simple API** through DBContext class
- **Automatic schema** creation and migration

For implementation details, see the model files in `mod/Model/` directory.
