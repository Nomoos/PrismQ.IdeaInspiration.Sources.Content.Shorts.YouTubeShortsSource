# Model - Database Layer for YouTube Video Data

This folder contains the SQLAlchemy ORM-based model layer for storing YouTube video data from yt-dlp in SQLite database.

## Overview

The model layer provides:
- **Raw yt-dlp data storage** - No data transformation, stores complete yt-dlp output
- **Type-safe database operations** using SQLAlchemy ORM
- **CRUD operations** (Create, Read, Update, Delete, Upsert)
- **Automatic schema management** - tables are created automatically
- **Simple API** for working with YouTube video data

## Components

### `base.py`
Defines the SQLAlchemy declarative base and naming conventions for database constraints.

### `youtube_video.py`
The main ORM model representing a YouTube video with raw yt-dlp data:
- `id` - Primary key
- `video_id` - YouTube video ID (unique, indexed)
- `raw_data` - Complete yt-dlp data as JSON string
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### `db_context.py`
Database context class providing CRUD operations:
- `create()` - Insert a new video record
- `read()` - Read by video_id
- `read_by_id()` - Read by database ID
- `update()` - Update an existing record
- `upsert()` - Insert or update (idempotent)
- `delete()` - Delete a record
- `list_all()` - List all records with filtering and sorting
- `count()` - Get total record count
- `clear_all()` - Delete all records

## Usage

### Basic CRUD Operations

```python
from Model import DBContext

# Sample yt-dlp data (complete output from yt-dlp)
ytdlp_data = {
    'id': 'abc123',
    'title': 'Amazing Short Video',
    'description': 'This is a great video',
    'uploader': 'Channel Name',
    'channel_id': 'UC...',
    'duration': 45,
    'view_count': 10000,
    'like_count': 500,
    # ... all other yt-dlp fields
}

# Create database context
db = DBContext('ideas.db')

# Create a new record (stores complete yt-dlp data)
record = db.create(
    video_id='abc123',
    ytdlp_data=ytdlp_data
)

# Read a record
record = db.read('abc123')
print(record.get_field('title'))  # Get specific field from yt-dlp data
print(record.get_field('view_count'))

# Get all yt-dlp data
full_data = record.get_raw_data()
print(full_data['uploader'])

# Update a record (with updated yt-dlp data)
updated_data = ytdlp_data.copy()
updated_data['view_count'] = 15000
db.update('abc123', updated_data)

# Upsert (insert or update)
db.upsert('xyz789', ytdlp_data)

# Delete a record
db.delete('abc123')

# List all records
records = db.list_all(limit=10)
for rec in records:
    print(f"{rec.get_field('title')}: {rec.get_field('view_count')} views")

# Close connection
db.close()
```

### Using as Context Manager

```python
from Model import DBContext

with DBContext('ideas.db') as db:
    # Your operations here
    record = db.upsert('video123', ytdlp_data)
    print(f"Saved: {record.get_field('title')}")
# Connection automatically closed
```

### Accessing yt-dlp Fields

```python
from Model import DBContext

db = DBContext('ideas.db')
record = db.read('abc123')

if record:
    # Get individual fields
    title = record.get_field('title')
    views = record.get_field('view_count', 0)  # with default
    uploader = record.get_field('uploader')
    
    # Get all raw data
    all_data = record.get_raw_data()
    
    # Access any yt-dlp field
    duration = all_data.get('duration')
    tags = all_data.get('tags', [])
    thumbnail = all_data.get('thumbnail')

db.close()
```

## Database Schema

The SQLAlchemy model creates the following table:

```sql
CREATE TABLE youtube_video (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id VARCHAR(255) NOT NULL UNIQUE,
    raw_data TEXT NOT NULL,  -- JSON string with complete yt-dlp data
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE INDEX ix_video_id ON youtube_video (video_id);
CREATE INDEX ix_created_at ON youtube_video (created_at);
```

## Database Initialization

Initialize the database using the init script:

```bash
# Initialize with default database path (ideas.db)
python scripts/init_db.py

# Initialize with custom database path
python scripts/init_db.py --db-path /path/to/database.db

# Quiet mode (no output)
python scripts/init_db.py --quiet
```

Or programmatically:

```python
from Model import DBContext

# Simply creating a DBContext instance initializes the database
db = DBContext('ideas.db')
# Tables are created automatically if they don't exist
db.close()
```

## Why Store Raw yt-dlp Data?

Storing the complete yt-dlp output as JSON has several advantages:

1. **No Data Loss** - All fields extracted by yt-dlp are preserved
2. **No Transformation** - Data is stored as-is from yt-dlp
3. **Flexibility** - Can access any field without schema changes
4. **Future-Proof** - New yt-dlp fields are automatically stored
5. **Easy Migration** - Raw data can be transformed later if needed

## Example yt-dlp Fields Available

When you store yt-dlp data, you get access to all these fields and more:

```python
{
    'id': 'video_id',
    'title': 'Video Title',
    'description': 'Video description',
    'uploader': 'Channel Name',
    'uploader_id': 'channel_id',
    'channel': 'Channel Name',
    'channel_id': 'UC...',
    'duration': 45,
    'view_count': 10000,
    'like_count': 500,
    'comment_count': 50,
    'thumbnail': 'https://...',
    'upload_date': '20250119',
    'timestamp': 1642550400,
    'tags': ['tag1', 'tag2'],
    'categories': ['Entertainment'],
    'width': 1080,
    'height': 1920,
    'fps': 30,
    # ... and many more fields
}
```

## Testing

Tests are available in `tests/test_new_model.py`:

```bash
# Run model tests
pytest tests/test_new_model.py -v
```

## Best Practices

1. **Always use context managers** when possible:
   ```python
   with DBContext('ideas.db') as db:
       # Your operations
       pass
   ```

2. **Use upsert for idempotent operations**:
   ```python
   db.upsert(video_id, ytdlp_data)  # Safe to call multiple times
   ```

3. **Store complete yt-dlp data**:
   ```python
   # Get complete yt-dlp output
   info = ydl.extract_info(url, download=False)
   # Store everything
   db.create(info['id'], info)
   ```

4. **Handle None results when reading**:
   ```python
   record = db.read('video123')
   if record:
       print(record.get_field('title'))
   else:
       print("Video not found")
   ```

## Troubleshooting

### IntegrityError: UNIQUE constraint failed

This occurs when trying to create a record with duplicate video_id. Use `upsert()` instead of `create()`.

### JSON Decode Error

Ensure you're passing a valid dictionary to `create()` or `update()`, not a JSON string.

### Table already exists

The model automatically creates tables if they don't exist. This is normal and safe to ignore.

## Integration with yt-dlp

Example of scraping and storing:

```python
import yt_dlp
from Model import DBContext

# Configure yt-dlp
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
}

# Create database
db = DBContext('ideas.db')

# Scrape and store
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # Extract info (no download)
    info = ydl.extract_info('https://youtube.com/watch?v=...', download=False)
    
    # Store complete yt-dlp data
    db.upsert(info['id'], info)
    
    print(f"Stored: {info['title']}")

db.close()
```
