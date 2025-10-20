# Database Model Layer

This folder contains the SQLAlchemy ORM-based model layer for storing YouTube Shorts data in SQLite database.

## Overview

The model layer provides:
- **Type-safe database operations** using SQLAlchemy ORM
- **CRUD operations** (Create, Read, Update, Delete, Upsert)
- **Automatic schema management** - tables are created automatically
- **Query builders** for common operations
- **Backward compatibility** with the legacy `Database` class

## Components

### `base.py`
Defines the SQLAlchemy declarative base and naming conventions for database constraints.

### `youtube_shorts_source.py`
The main ORM model representing a YouTube Shorts record with fields:
- `id` - Primary key
- `source` - Source platform (e.g., 'youtube')
- `source_id` - Unique identifier from the source
- `title` - Video title
- `description` - Video description
- `tags` - Comma-separated tags
- `score` - Calculated score
- `score_dictionary` - JSON string of score components
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### `db_context.py`
Database context class providing CRUD operations:
- `create()` - Insert a new record
- `read()` - Read by source and source_id
- `read_by_id()` - Read by database ID
- `update()` - Update an existing record
- `upsert()` - Insert or update (insert if new, update if exists)
- `delete()` - Delete a record
- `list_all()` - List all records with optional filtering and sorting
- `count()` - Get total record count
- `count_by_source()` - Count records by source
- `clear_all()` - Delete all records

## Usage

### Basic CRUD Operations

```python
from mod.Model import DBContext

# Create database context
db = DBContext('ideas.db')

# Create a new record
record = db.create(
    source='youtube',
    source_id='abc123',
    title='Amazing Video',
    description='This is a great video',
    tags='inspiration,ideas',
    score=85.5,
    score_dictionary={'views': 1000, 'likes': 50}
)

# Read a record
record = db.read('youtube', 'abc123')
print(record.title)  # Output: Amazing Video

# Update a record
updated = db.update(
    source='youtube',
    source_id='abc123',
    title='Updated Title',
    score=90.0
)

# Upsert (insert or update)
record = db.upsert(
    source='youtube',
    source_id='xyz789',
    title='New or Updated Video',
    score=75.0
)

# Delete a record
deleted = db.delete('youtube', 'abc123')

# List all records
records = db.list_all(limit=10, order_by='score', ascending=False)
for record in records:
    print(f"{record.title}: {record.score}")

# Get record count
total = db.count()
youtube_count = db.count_by_source('youtube')

# Clear all records
db.clear_all()

# Close connection
db.close()
```

### Using as Context Manager

```python
from mod.Model import DBContext

with DBContext('ideas.db') as db:
    record = db.create(
        source='youtube',
        source_id='test123',
        title='Test Video'
    )
    print(f"Created: {record.title}")
# Connection automatically closed
```

### Working with Score Dictionary

```python
from mod.Model import DBContext

db = DBContext('ideas.db')

# Create with score dictionary
score_data = {
    'engagement_rate': 0.85,
    'views': 10000,
    'likes': 500,
    'comments': 50
}

record = db.create(
    source='youtube',
    source_id='video123',
    title='My Video',
    score_dictionary=score_data
)

# Retrieve and use score dictionary
retrieved = db.read('youtube', 'video123')
score_dict = retrieved.get_score_dict()
print(f"Engagement rate: {score_dict['engagement_rate']}")

# Update score dictionary
new_score_data = {
    'engagement_rate': 0.90,
    'views': 15000,
    'likes': 750,
    'comments': 100
}
retrieved.set_score_dict(new_score_data)

db.close()
```

### Converting to Dictionary

```python
from mod.Model import DBContext

db = DBContext('ideas.db')

record = db.read('youtube', 'abc123')
if record:
    # Convert to dictionary for JSON serialization
    data = record.to_dict()
    print(data)
    # {
    #     'id': 1,
    #     'source': 'youtube',
    #     'source_id': 'abc123',
    #     'title': 'Amazing Video',
    #     'description': 'This is a great video',
    #     'tags': 'inspiration,ideas',
    #     'score': 85.5,
    #     'score_dictionary': '{"views": 1000, "likes": 50}',
    #     'created_at': '2025-01-15T10:30:00+00:00',
    #     'updated_at': '2025-01-15T10:30:00+00:00'
    # }

db.close()
```

## Database Initialization

You can initialize the database using the `init_db.py` script:

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
from mod.Model import DBContext

# Simply creating a DBContext instance initializes the database
db = DBContext('ideas.db')
# Tables are created automatically if they don't exist
db.close()
```

## Backward Compatibility

The legacy `Database` class in `mod/database.py` has been updated to use this model layer internally while maintaining the same API. This ensures existing code continues to work without modifications.

```python
# Old code still works
from mod.database import Database

db = Database('ideas.db')
db.insert_idea(
    source='youtube',
    source_id='abc123',
    title='Test Video',
    score=85.0
)
ideas = db.get_all_ideas(limit=10)
db.close()
```

## Schema

The SQLAlchemy model creates the following table:

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
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE (source, source_id)
);

CREATE INDEX ix_source_source_id ON youtube_shorts_source (source, source_id);
CREATE INDEX ix_score ON youtube_shorts_source (score);
CREATE INDEX ix_created_at ON youtube_shorts_source (created_at);
```

## Testing

Comprehensive tests are available in `tests/test_model.py`:

```bash
# Run model tests
pytest tests/test_model.py -v

# Run with coverage
pytest tests/test_model.py --cov=mod.Model --cov-report=html
```

## Best Practices

1. **Always use context managers** when possible to ensure proper cleanup:
   ```python
   with DBContext('ideas.db') as db:
       # Your operations
       pass
   ```

2. **Use upsert for idempotent operations** when you want to create or update:
   ```python
   db.upsert(source='youtube', source_id='abc', title='Video')
   ```

3. **Validate data before inserting** to avoid database errors:
   ```python
   if title and source_id:
       db.create(source='youtube', source_id=source_id, title=title)
   ```

4. **Handle None results** when reading:
   ```python
   record = db.read('youtube', 'abc123')
   if record:
       print(record.title)
   else:
       print("Record not found")
   ```

5. **Use score_dictionary for complex metrics**:
   ```python
   score_dict = {
       'engagement_rate': 0.85,
       'views_per_day': 1000,
       'like_ratio': 0.05
   }
   db.create(..., score_dictionary=score_dict)
   ```

## Migration from Legacy Database

If you have existing data in the old `ideas` table, both tables can coexist. The `Database` class wrapper ensures data is written to the new `youtube_shorts_source` table while maintaining compatibility.

To migrate existing data:

```python
import sqlite3
from mod.Model import DBContext

# Connect to database
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
```

## Troubleshooting

### IntegrityError: UNIQUE constraint failed

This occurs when trying to create a record with duplicate (source, source_id). Use `upsert()` instead of `create()`.

### Table already exists

The model automatically creates tables if they don't exist. If you see this error, it's safe to ignore.

### PendingRollbackError

This indicates a previous transaction failed. The `create()` method now properly handles this by rolling back on IntegrityError.

## Future Enhancements

Potential improvements for this model layer:
- Add migration support with Alembic
- Implement soft deletes
- Add full-text search capabilities
- Support for multiple source types with polymorphic models
- Query result caching
- Bulk insert/update operations
