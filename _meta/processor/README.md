# Processor Module

This module provides functionality to transform YouTube Shorts data from the `YouTubeShortsSource` database model into the standardized `IdeaInspiration` format as defined in [PrismQ.IdeaInspiration.Model](https://github.com/Nomoos/PrismQ.IdeaInspiration.Model).

## Overview

The processor bridges the gap between platform-specific data storage (YouTube Shorts) and the unified PrismQ content model. It transforms raw scraped data into a standardized format suitable for scoring, classification, and content generation.

## Architecture

```
YouTubeShortsSource (Database) → IdeaProcessor → IdeaInspiration (Standard Model)
```

### Data Flow

1. **Input**: `YouTubeShortsSource` database records with YouTube-specific fields
2. **Transformation**: `IdeaProcessor` converts platform-specific data to universal format
3. **Output**: `IdeaInspiration` instances ready for downstream processing

## Features

- 🔄 **Complete Transformation**: Converts all YouTube Shorts metadata to standardized format
- 📊 **Metadata Mapping**: Intelligently maps YouTube statistics to universal metadata
- 📝 **Content Extraction**: Extracts subtitles as content for text analysis
- 🏷️ **Keyword Processing**: Converts comma-separated tags to keyword lists
- ✅ **Processing Status**: Marks records as processed to prevent duplicate transformations
- 📦 **Batch Processing**: Efficiently process multiple records
- 💾 **JSON Export**: Export processed ideas to JSON files

## Field Mapping

### Basic Fields
| YouTubeShortsSource | IdeaInspiration | Description |
|---------------------|-----------------|-------------|
| `title` | `title` | Video title |
| `description` | `description` | Video description |
| `tags` | `keywords` | Comma-separated tags → List |
| `source_id` | `source_id` | YouTube video ID |
| `score` | `score` | Engagement score (rounded to int) |
| N/A | `source_type` | Set to "video" for all YouTube Shorts |
| N/A | `source_url` | Generated: `https://www.youtube.com/shorts/{id}` |

### Content Field
| Source | Destination | Description |
|--------|-------------|-------------|
| `score_dictionary.enhanced_metrics.subtitle_text` | `content` | Subtitle/transcription text |

### Source Information
| Source | Destination | Description |
|--------|-------------|-------------|
| `score_dictionary.snippet.channelTitle` | `source_created_by` | Channel name |
| `score_dictionary.snippet.publishedAt` | `source_created_at` | Upload date (ISO 8601) |

### Metadata Dictionary (String Key-Value Pairs)

#### Statistics
- `views`: View count
- `likes`: Like count  
- `comments`: Comment count

#### Content Details
- `duration`: Video duration (ISO 8601 format)

#### Enhanced Metrics
- `engagement_rate`: Calculated engagement percentage
- `views_per_day`: Average views per day
- `resolution`: Video resolution (e.g., "1080x1920")
- `fps`: Frames per second
- `aspect_ratio`: Aspect ratio (e.g., "9:16")
- `subtitles_available`: Whether subtitles exist
- `channel_follower_count`: Channel subscriber count

#### Channel Information
- `channel_id`: YouTube channel ID
- `channel_title`: Channel name
- `category_id`: YouTube category ID
- `published_at`: Upload date

#### Platform Identifiers
- `platform`: Always "youtube_shorts"
- `source_type`: Always "video"

## Usage

### Command Line Interface

#### Process All Unprocessed Records
```bash
python -m cli process
```

#### Process Limited Number of Records
```bash
python -m cli process --limit 10
```

#### Export to JSON File
```bash
python -m cli process --output processed_ideas.json
```

### Python API

#### Process Single Record
```python
from Model.db_context import DBContext
from processor.idea_processor import IdeaProcessor

# Get record from database
db = DBContext('ideas.db')
with db.get_session() as session:
    from Model.youtube_shorts_source import YouTubeShortsSource
    record = session.query(YouTubeShortsSource).filter_by(processed=False).first()

# Transform to IdeaInspiration
idea = IdeaProcessor.process(record)

# Access transformed data
print(f"Title: {idea.title}")
print(f"Content: {idea.content[:100]}...")
print(f"Keywords: {idea.keywords}")
print(f"Source URL: {idea.source_url}")
print(f"Metadata: {idea.metadata}")

# Convert to dictionary
idea_dict = idea.to_dict()
```

#### Batch Processing
```python
from Model.db_context import DBContext
from processor.idea_processor import IdeaProcessor

# Get unprocessed records
db = DBContext('ideas.db')
with db.get_session() as session:
    from Model.youtube_shorts_source import YouTubeShortsSource
    records = session.query(YouTubeShortsSource).filter_by(processed=False).limit(100).all()

# Process in batch
ideas = IdeaProcessor.process_batch(records)

# Process results
for idea in ideas:
    print(f"Processed: {idea.title}")
    # Use idea for scoring, classification, etc.
```

#### Mark Records as Processed
```python
from Model.db_context import DBContext

db = DBContext('ideas.db')
with db.get_session() as session:
    from Model.youtube_shorts_source import YouTubeShortsSource
    record = session.query(YouTubeShortsSource).filter_by(source_id='video_id').first()
    
    # Mark as processed
    record.processed = True
    session.commit()
```

## Integration with PrismQ Ecosystem

The processor is designed to integrate seamlessly with other PrismQ modules:

### With Scoring Module
```python
from processor.idea_processor import IdeaProcessor
from prismq.idea.scoring import ScoringEngine

# Transform and score
idea = IdeaProcessor.process(record)
scoring_engine = ScoringEngine()
score = scoring_engine.score_idea_inspiration(idea)
```

### With Classification Module
```python
from processor.idea_processor import IdeaProcessor
from prismq.idea.classification import TextClassifier

# Transform and classify
idea = IdeaProcessor.process(record)
classifier = TextClassifier()
category = classifier.classify(idea)
```

## Error Handling

The processor includes comprehensive error handling:

### Validation Errors
```python
try:
    idea = IdeaProcessor.process(record)
except ValueError as e:
    print(f"Validation error: {e}")
    # Handle missing required fields
```

### Batch Processing Errors
```python
# Batch processing continues on error
ideas = IdeaProcessor.process_batch(records)
# Failed records are skipped with warning
# Successful transformations are returned
```

## Testing

The processor includes comprehensive test coverage:

```bash
# Run processor tests
pytest tests/test_processor.py -v

# Run with coverage
pytest tests/test_processor.py --cov=processor --cov-report=html
```

Test categories:
- ✅ Basic transformations with minimal data
- ✅ Full metadata transformations
- ✅ Subtitle/content extraction
- ✅ Edge cases and error handling
- ✅ Batch processing
- ✅ Date format conversions

## Performance Considerations

- **Batch Processing**: Use `process_batch()` for efficient bulk transformations
- **Memory Usage**: Process in chunks for large datasets
- **Database Sessions**: Uses context managers for proper session cleanup
- **Validation**: Minimal validation for performance (title, source_id only)

## Best Practices

1. **Process After Scraping**: Run processor after collecting new YouTube Shorts
2. **Check Processed Status**: Query for `processed=False` to avoid duplicates
3. **Export Regularly**: Save processed ideas to JSON for backup
4. **Error Logging**: Monitor warnings for failed transformations
5. **Batch Size**: Process 100-1000 records at a time for optimal performance

## Implementation Details

### IdeaInspiration Model

The processor uses a lightweight version of the IdeaInspiration model that matches the specification from PrismQ.IdeaInspiration.Model. This ensures compatibility without requiring the full package as a dependency.

### Metadata Format

All metadata is stored as string key-value pairs for SQLite compatibility, following the specification in PrismQ.IdeaInspiration.Model.

### Date Handling

The processor automatically converts YouTube date formats:
- YYYYMMDD → ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- ISO 8601 → Preserved as-is
- Invalid → Returned as-is with warning

## Future Enhancements

Potential improvements:
- Support for additional metadata fields
- Custom field mapping configurations
- Async batch processing
- Progress bars for large batches
- Retry logic for failed transformations
- Validation against JSON schema

## Related Modules

- **[PrismQ.IdeaInspiration.Model](https://github.com/Nomoos/PrismQ.IdeaInspiration.Model)** - Standard model specification
- **[PrismQ.IdeaInspiration.Scoring](https://github.com/Nomoos/PrismQ.IdeaInspiration.Scoring)** - Content scoring engine
- **[PrismQ.IdeaInspiration.Classification](https://github.com/Nomoos/PrismQ.IdeaInspiration.Classification)** - Content classification

## License

This repository is proprietary software. All Rights Reserved - Copyright (c) 2025 PrismQ
