# PrismQ YouTube Shorts Source

A powerful tool for scraping YouTube Shorts content with comprehensive metadata extraction and universal metrics collection.

> **Platform Support**: Optimized for Windows with NVIDIA RTX GPUs. Limited Linux support available for development.
## Features

- **YouTube Shorts Scraping**: Multiple powerful scraping modes
  - **Search-based scraping**: Uses YouTube API to search for Shorts by keywords
  - **Channel-based scraping**: Uses yt-dlp to scrape Shorts from specific YouTube channels
  - **Trending scraping**: Uses yt-dlp to scrape Shorts from YouTube trending page
  - **Keyword scraping**: Uses yt-dlp to search and scrape Shorts by keywords
  - Filters for videos up to 3 minutes (180 seconds) 
  - Validates vertical format (height > width) for true Shorts
  - Extracts comprehensive video metadata and statistics
  - Supports pagination and configurable result limits
  
- **Enhanced Metadata Extraction** (channel scraping with yt-dlp):
  - **Subtitle extraction and parsing**: Automatic subtitle download and conversion to plain text
  - **Video quality metrics**: Resolution, FPS, aspect ratio
  - **Engagement analytics**: Views per day/hour, engagement rates, like-to-view ratios
  - **Channel information**: Channel ID, name, subscriber count
  - **Content analysis**: Title/description length, tag counts
  
- **Universal Metrics Collection**: Standardized metrics for cross-platform analysis
  - Engagement metrics (views, likes, comments, shares)
  - Calculated metrics (engagement rate, like-to-view ratio, etc.)
  - Platform-specific metrics preserved
  - See [METRICS.md](docs/METRICS.md) for complete documentation
  
- **Deduplication**: Automatically prevents duplicate ideas using (source, source_id) unique constraint
  
- **SQLite Storage**: Stores ideas with complete metadata:
  - Title
  - Description
  - Tags
  - Universal metrics (JSON format)
  - Enhanced metrics (engagement analytics)
  - Source information
  
- **Simple Configuration**: 
  - Single `.env` file per working directory for all settings
  - **Automatic working directory management** - Never manually specify directories
  - Each directory maintains its own independent configuration
  - Settings automatically persisted and remembered

- **Interactive Mode**: Quickstart scripts with interactive configuration for easy setup

- **Windows Compatible**: Designed to work seamlessly on Windows systems

- **IdeaInspiration Processor**: Transform scraped data to standardized format
  - Converts YouTubeShortsSource records to IdeaInspiration model
  - Compatible with [PrismQ.IdeaInspiration.Model](https://github.com/Nomoos/PrismQ.IdeaInspiration.Model)
  - Intelligent metadata mapping for cross-platform compatibility
  - Batch processing support with progress tracking
  - JSON export capability for downstream processing
  - See [processor/README.md](processor/README.md) for complete documentation

## Documentation

For comprehensive documentation, see:

- **[docs/](docs/)** - User and developer documentation
  - **[⚙️ Configuration Guide](docs/CONFIGURATION.md)** - Working directories, .env management, and all settings
  - [Contributing Guidelines](docs/CONTRIBUTING.md)
  - [Metrics Documentation](docs/METRICS.md)
  - **[🗄️ YouTube Data Model (YTB_DATA_MODEL.md)](docs/YTB_DATA_MODEL.md)** - Complete SQLite database schema and storage documentation
  - [Model Implementation](docs/MODEL_IMPLEMENTATION.md) - SQLAlchemy ORM implementation details
  - **[📊 Data Collection Suite](docs/DATA_COLLECTION_INDEX.md)** - Complete guide to what data we collect
    - [Guide](docs/DATA_COLLECTION_GUIDE.md) - Decision trees & FAQs
    - [Summary](docs/DATA_COLLECTION_SUMMARY.md) - Quick reference
    - [Analysis](docs/DATA_COLLECTION_ANALYSIS.md) - Comprehensive details
    - [Diagram](docs/DATA_COLLECTION_DIAGRAM.md) - Visual representations
    - [Field Reference](docs/DATA_FIELDS_REFERENCE.md) - Complete catalog
  - [Scraping Best Practices](docs/SCRAPING_BEST_PRACTICES.md) - Safety, re-scraping, and alternatives
  - [Windows Quickstart Guide](docs/WINDOWS_QUICKSTART.md)
- **[issues/](issues/)** - File-based issue tracking
  - [Issue Tracking Guide](issues/README.md)
  - [Known Issues](issues/KNOWN_ISSUES.md)
  - [Project Roadmap](issues/ROADMAP.md)
- **[scripts/](scripts/)** - Setup and utility scripts
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Build, test, and development guide

## Installation

### Prerequisites

- Python 3.10 or higher (required)
- pip package manager
- Windows OS (recommended)
- NVIDIA GPU with CUDA support (optional, for future AI features)

### Quick Start (Recommended)

#### Windows

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nomoos/PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource
   ```

2. **Run setup**:
   ```batch
   scripts\setup.bat
   ```

3. **Run quickstart**:
   ```batch
   scripts\quickstart.bat
   ```

The quickstart script will guide you through:
- Interactive configuration (if no .env file exists)
- Scraping YouTube Shorts
- Viewing collected ideas

#### Linux/Mac

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nomoos/PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource
   ```

2. **Run setup**:
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Run quickstart**:
   ```bash
   chmod +x scripts/quickstart.sh
   ./scripts/quickstart.sh
   ```

### Manual Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nomoos/PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env  # On Windows
     # or
     cp .env.example .env    # On Linux/Mac
     ```
   
   - Edit `.env` and add your API credentials:
     - **YouTube API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/)

## Configuration

Edit the `.env` file to customize the application:

```ini
# Database Configuration
DATABASE_PATH=ideas.db

# YouTube API Configuration (for search-based scraping)
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_MAX_RESULTS=50

# YouTube Channel Configuration (for channel-based scraping with yt-dlp)
# Example: https://www.youtube.com/@channelname or @channelname or UC1234567890
YOUTUBE_CHANNEL_URL=
YOUTUBE_CHANNEL_MAX_SHORTS=10

# YouTube Trending Configuration (for trending scraping with yt-dlp)
YOUTUBE_TRENDING_MAX_SHORTS=10

# YouTube Keyword Configuration (for keyword search with yt-dlp)
YOUTUBE_KEYWORD_MAX_SHORTS=10
```

### Scraping Modes

> **⚠️ Recommendation**: Use yt-dlp-based methods (channel, trending, keyword) for data mining. They provide richer metadata, no API quota limits, and don't require an API key. The API-based `scrape` command is maintained for backward compatibility only.

#### Channel-Based Scraping (yt-dlp) ⭐ **Recommended**
Uses yt-dlp to scrape comprehensive metadata from specific YouTube channels. No API key required, but requires yt-dlp to be installed.

```bash
# Scrape from a specific channel
python -m src.cli scrape-channel --channel @channelname

# Scrape a specific number of shorts
python -m src.cli scrape-channel --channel @channelname --top 20
```

#### Trending Scraping (yt-dlp) ⭐ **Recommended**
Uses yt-dlp to scrape Shorts from YouTube trending page. No API key required.

```bash
# Scrape from trending
python -m src.cli scrape-trending
```

#### Keyword Scraping (yt-dlp) ⭐ **Recommended**
Uses yt-dlp to search and scrape Shorts by keywords. No API key required.

```bash
# Scrape by keyword
python -m src.cli scrape-keyword --keyword "startup ideas"

# Scrape with more results
python -m src.cli scrape-keyword --keyword "business tips" --top 20
```

#### Search-Based Scraping (YouTube API) - Legacy
Uses YouTube Data API v3 to search for Shorts by keywords. **Not recommended for data mining** - use yt-dlp methods instead. Kept for backward compatibility.

**Limitations:**
- Requires YouTube API key
- Subject to 10,000 units/day quota
- Limited metadata (no subtitles, quality metrics, or enhanced analytics)
- Cannot access trending page

```bash
python -m src.cli scrape
```

---

**Why yt-dlp methods are recommended (channel, trending, keyword):**
- ✅ Comprehensive metadata including subtitles
- ✅ Video quality metrics (resolution, FPS, aspect ratio)
- ✅ Engagement analytics (views per day/hour)
- ✅ No API quota limits
- ✅ Works without YouTube API key
- ✅ Direct access to trending page


## Usage

### Scrape Ideas

> **⚠️ Recommendation**: Use yt-dlp-based commands (channel, trending, keyword) for best results. They provide richer metadata and no API limits.

#### Channel-Based Scraping ⭐ **Recommended**
Scrape YouTube Shorts from a specific channel using yt-dlp:

```bash
# Basic usage with channel handle
python -m src.cli scrape-channel --channel @channelname

# Using full channel URL
python -m src.cli scrape-channel --channel https://www.youtube.com/@channelname

# Using channel ID
python -m src.cli scrape-channel --channel UC1234567890

# Scrape specific number of shorts
python -m src.cli scrape-channel --channel @channelname --top 20
```

**Channel scraping features:**
- Extracts subtitles and converts to plain text
- Captures video quality metrics (resolution, FPS, aspect ratio)
- Calculates engagement metrics (views per day/hour)
- Filters for true Shorts (≤3 min, vertical format)
- No API quota limits

#### Trending Scraping
Scrape Shorts from YouTube trending page:

```bash
# Basic usage
python -m src.cli scrape-trending

# Scrape more shorts
python -m src.cli scrape-trending --top 20
```

**Trending scraping features:**
- No API key required
- Discover viral and trending content
- Same rich metadata as channel scraping

#### Keyword Scraping
Search and scrape Shorts by keywords:

```bash
# Basic keyword search
python -m src.cli scrape-keyword --keyword "startup ideas"

# Search with more results
python -m src.cli scrape-keyword --keyword "business tips" --top 20
```

**Keyword scraping features:**
- Search any topic or niche
- No API key required
- Automatic Shorts filtering
- Same rich metadata as other yt-dlp modes

---

#### Search-Based Scraping (YouTube API - Legacy)
**⚠️ NOT RECOMMENDED**: Use yt-dlp methods above instead. This command is kept for backward compatibility.

```bash
# Basic API-based search (legacy)
python -m src.cli scrape

# Use a custom .env file
python -m src.cli scrape --env-file /path/to/.env
```

**Limitations:**
- Requires YouTube API key (subject to 10,000 units/day quota)
- Limited metadata (no subtitles, quality metrics, or enhanced analytics)
- Cannot access trending page or specific channels
- Less comprehensive than yt-dlp methods

**Why yt-dlp is better:**
- ✅ No API quota limits
- ✅ Richer metadata (subtitles, quality metrics, engagement analytics)
- ✅ Works without API key
- ✅ Direct trending and channel access

---

### Process to IdeaInspiration Format

Transform scraped YouTube Shorts records to the standardized IdeaInspiration model:

```bash
# Process all unprocessed records
python -m cli process

# Process limited number of records
python -m cli process --limit 10

# Export processed ideas to JSON
python -m cli process --output processed_ideas.json
```

**What it does:**
- Converts YouTubeShortsSource records to IdeaInspiration format
- Extracts subtitles as content for text analysis
- Maps YouTube metadata to universal format
- Marks records as `processed=True` to prevent reprocessing
- Compatible with PrismQ.IdeaInspiration.Scoring and Classification modules

See [processor/README.md](processor/README.md) for detailed documentation and Python API usage.

---

### List Ideas

List the top ideas (default: 20):
```bash
python -m src.cli list
```

Show more results:
```bash
python -m src.cli list --limit 50
```

Filter by source:
```bash
python -m src.cli list --source youtube
```

### View Statistics

View collection statistics:
```bash
python -m src.cli stats
```

### Clear Database

Clear all collected ideas:
```bash
python -m src.cli clear
```

## Database Schema

The application uses a **SQLAlchemy ORM-based model layer** for robust, type-safe database operations. Data is stored in SQLite with two table structures.

> **📚 For complete documentation**, see **[YouTube Data Model (YTB_DATA_MODEL.md)](docs/YTB_DATA_MODEL.md)** which includes:
> - Complete schema documentation
> - Field descriptions and constraints
> - Data flow and transformation pipeline
> - Query patterns and examples
> - Performance optimization tips
> - Migration and backup procedures

### Modern ORM Model (Recommended)
Uses SQLAlchemy ORM with the `DBContext` class for CRUD operations:

```python
from mod.Model import DBContext

# Create and use database context
with DBContext('ideas.db') as db:
    # Upsert (insert or update)
    record = db.upsert(
        source='youtube',
        source_id='abc123',
        title='Video Title',
        score=85.5,
        score_dictionary={'views': 1000, 'likes': 50}
    )
    
    # Read records
    record = db.read('youtube', 'abc123')
    records = db.list_all(limit=10, order_by='score')
```

**Table: `youtube_shorts_source`**
```sql
CREATE TABLE youtube_shorts_source (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source VARCHAR(100) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    score FLOAT,
    score_dictionary TEXT,  -- JSON string
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE(source, source_id)
);
```

### Legacy Database Class (Backward Compatible)
The original `Database` class now wraps the ORM model for backward compatibility:

```python
from mod.database import Database

db = Database('ideas.db')
db.insert_idea(source='youtube', source_id='abc123', title='Video')
ideas = db.get_all_ideas(limit=10)
db.close()
```

**Table: `ideas`** (maintained for compatibility)

See [mod/Model/README.md](mod/Model/README.md) for model layer documentation and [docs/YTB_DATA_MODEL.md](docs/YTB_DATA_MODEL.md) for complete database documentation.

### Database Initialization

Initialize the database schema using the init script:

```bash
# Initialize with default path
python scripts/init_db.py

# Initialize with custom path
python scripts/init_db.py --db-path /path/to/database.db
```

The database is also initialized automatically when you first run any scraping command.

## Extending for Other Platforms

This repository is part of the PrismQ Idea Sources taxonomy. To add support for other platforms:

1. Create a new repository following the naming pattern:
   - `PrismQ.IdeaInspiration.Sources.Content.Shorts.TikTokSource`
   - `PrismQ.IdeaInspiration.Sources.Content.Forums.RedditSource`
   - etc.

2. Implement the `SourcePlugin` interface

3. Use the universal metrics system for cross-platform compatibility

See the [PrismQ.RepositoryTemplate](https://github.com/Nomoos/PrismQ.RepositoryTemplate) for module structure guidelines.

## Development

### Running Tests

Run the test suite:
```bash
pytest
```

With coverage:
```bash
pytest --cov=src --cov-report=html
```

### Project Structure

```
PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource/
├── mod/                    # Main module package
│   ├── cli.py              # Command-line interface (with process command)
│   ├── config.py           # Configuration management
│   ├── logging_config.py   # Logging configuration
│   ├── database.py         # Legacy database wrapper (backward compatible)
│   ├── metrics.py          # Universal metrics system
│   ├── Model/              # SQLAlchemy ORM model layer
│   │   ├── __init__.py
│   │   ├── base.py         # SQLAlchemy base configuration
│   │   ├── youtube_shorts_source.py  # ORM model (with processed field)
│   │   ├── db_context.py   # Database context with CRUD operations
│   │   └── README.md       # Model documentation
│   └── sources/            # Source plugins
│       ├── __init__.py     # Base plugin interface
│       ├── youtube_plugin.py
│       ├── youtube_channel_plugin.py
│       └── youtube_trending_plugin.py
├── processor/              # IdeaInspiration transformation module
│   ├── __init__.py
│   ├── idea_processor.py   # Core transformation logic
│   └── README.md           # Processor documentation
├── tests/                  # Unit and integration tests
│   ├── test_model.py       # Model layer tests
│   ├── test_database.py    # Legacy database tests
│   ├── test_processor.py   # Processor transformation tests
│   ├── test_config.py
│   └── test_metrics.py
├── scripts/                # Setup and utility scripts
│   ├── init_db.py          # Database initialization script
│   ├── setup.bat           # Windows setup
│   ├── setup.sh            # Linux/Mac setup
│   └── quickstart.bat/sh   # Interactive quickstart
├── docs/                   # Documentation
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   ├── METRICS.md          # Metrics documentation
│   └── WINDOWS_QUICKSTART.md
├── issues/                 # File-based issue tracking
├── .env.example            # Example configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## Guidelines

When modifying modules:

1. **Single Responsibility**: Each module focuses on a specific concern
2. **Dependency Management**: Depend on `src/` infrastructure (config, logging)
3. **Testing**: Update corresponding tests in `tests/`
4. **Documentation**: Keep docstrings and documentation up-to-date
5. **Code Quality**: Follow PEP 8 and use type hints

## Related Documentation

- Main README: `/README.md`
- Contributing Guidelines: `/docs/CONTRIBUTING.md`
- Copilot Instructions: `/.github/copilot-instructions.md`
