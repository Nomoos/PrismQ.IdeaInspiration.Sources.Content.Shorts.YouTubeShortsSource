# PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource

A PrismQ module for gathering idea inspirations from YouTube Shorts and storing them in a SQLite database for later analysis. Part of the PrismQ AI-powered content generation ecosystem.

## 🎯 Purpose

This module serves as a specialized YouTube Shorts scraping component of the PrismQ Ideas Sources ecosystem. It focuses on gathering video content inspiration from YouTube Shorts to fuel automated content generation pipelines.

### Related PrismQ Projects

- **[PrismQ.RepositoryTemplate](https://github.com/Nomoos/PrismQ.RepositoryTemplate)** - Template for PrismQ modules
- **[StoryGenerator](https://github.com/Nomoos/StoryGenerator)** - Automated story and video generation pipeline
- **Other PrismQ Idea Sources** - Specialized scrapers for different content types and platforms

## 💻 Target Platform

This module is optimized for:
- **Operating System**: Windows (primary), Linux (development support)
- **GPU**: NVIDIA RTX 5090 (32GB VRAM) for AI workloads
- **CPU**: AMD Ryzen processor (multi-core)
- **RAM**: 64GB DDR5
- **Python**: 3.10 or higher

> **Note for Linux users**: Limited Linux support is available for development purposes. macOS is not officially supported.

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
  
- **Simple Configuration**: Single `.env` file for all settings

- **Interactive Mode**: Quickstart scripts with interactive configuration for easy setup

- **Windows Compatible**: Designed to work seamlessly on Windows systems

## Documentation

For comprehensive documentation, see:

- **[docs/](docs/)** - User and developer documentation
  - [Contributing Guidelines](docs/CONTRIBUTING.md)
  - [Metrics Documentation](docs/METRICS.md)
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
   git clone https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource
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
   git clone https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource
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
   git clone https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource
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
YOUTUBE_CHANNEL_STORY_ONLY=false

# YouTube Trending Configuration (for trending scraping with yt-dlp)
YOUTUBE_TRENDING_MAX_SHORTS=10
YOUTUBE_TRENDING_STORY_ONLY=false

# YouTube Keyword Configuration (for keyword search with yt-dlp)
YOUTUBE_KEYWORD_MAX_SHORTS=10
YOUTUBE_KEYWORD_STORY_ONLY=false
```

### Scraping Modes

> **⚠️ Recommendation**: Use yt-dlp-based methods (channel, trending, keyword) for data mining. They provide richer metadata, no API quota limits, and don't require an API key. The API-based `scrape` command is maintained for backward compatibility only.

#### Channel-Based Scraping (yt-dlp) ⭐ **Recommended**
Uses yt-dlp to scrape comprehensive metadata from specific YouTube channels. No API key required, but requires yt-dlp to be installed.

```bash
# Scrape from a specific channel
python -m src.cli scrape-channel --channel @channelname

# Scrape with story detection filtering
python -m src.cli scrape-channel --channel @channelname --story-only

# Scrape a specific number of shorts
python -m src.cli scrape-channel --channel @channelname --top 20
```

#### Trending Scraping (yt-dlp) ⭐ **Recommended**
Uses yt-dlp to scrape Shorts from YouTube trending page. No API key required.

```bash
# Scrape from trending
python -m src.cli scrape-trending

# Scrape with story filtering
python -m src.cli scrape-trending --story-only --top 15
```

#### Keyword Scraping (yt-dlp) ⭐ **Recommended**
Uses yt-dlp to search and scrape Shorts by keywords. No API key required.

```bash
# Scrape by keyword
python -m src.cli scrape-keyword --keyword "startup ideas"

# Scrape with more results
python -m src.cli scrape-keyword --keyword "business tips" --top 20

# Scrape story videos only
python -m src.cli scrape-keyword --keyword "story time" --story-only
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

# Filter for story videos only
python -m src.cli scrape-channel --channel @channelname --story-only

# Combine options
python -m src.cli scrape-channel --channel @channelname --top 15 --story-only
```

**Channel scraping features:**
- Extracts subtitles and converts to plain text
- Captures video quality metrics (resolution, FPS, aspect ratio)
- Calculates engagement metrics (views per day/hour)
- Detects story videos with confidence scoring
- Filters for true Shorts (≤3 min, vertical format)
- No API quota limits

#### Trending Scraping
Scrape Shorts from YouTube trending page:

```bash
# Basic usage
python -m src.cli scrape-trending

# Scrape more shorts
python -m src.cli scrape-trending --top 20

# Filter for story videos only
python -m src.cli scrape-trending --story-only

# Combine options
python -m src.cli scrape-trending --top 15 --story-only
```

**Trending scraping features:**
- No API key required
- Discover viral and trending content
- Same rich metadata as channel scraping
- Story detection filtering available

#### Keyword Scraping
Search and scrape Shorts by keywords:

```bash
# Basic keyword search
python -m src.cli scrape-keyword --keyword "startup ideas"

# Search with more results
python -m src.cli scrape-keyword --keyword "business tips" --top 20

# Search for story content
python -m src.cli scrape-keyword --keyword "story time" --story-only

# Combine options
python -m src.cli scrape-keyword --keyword "tech news" --top 15 --story-only
```

**Keyword scraping features:**
- Search any topic or niche
- No API key required
- Automatic Shorts filtering
- Story detection filtering available
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
- ✅ Story detection with confidence scoring
- ✅ Works without API key
- ✅ Direct trending and channel access

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

The SQLite database uses the following schema:

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, source_id)
);
```

## Extending for Other Platforms

This repository is part of the PrismQ Idea Sources taxonomy. To add support for other platforms:

1. Create a new repository following the naming pattern:
   - `PrismQ.Idea.Sources.Content.Shorts.TikTokSource`
   - `PrismQ.Idea.Sources.Content.Forums.RedditSource`
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
PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource/
├── src/         # Main application package
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   ├── metrics.py          # Universal metrics system
│   ├── scoring/            # Scoring engine
│   └── sources/            # Source plugins
│       ├── __init__.py     # Base plugin interface
│       └── youtube_plugin.py
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_metrics.py
│   └── test_scoring.py
├── docs/                   # Documentation
│   ├── README.md
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   ├── METRICS.md          # Metrics documentation
│   └── WINDOWS_QUICKSTART.md
├── scripts/                # Setup and utility scripts
│   ├── README.md
│   ├── setup.bat           # Windows setup script
│   ├── setup.sh            # Linux/Mac setup script
│   ├── quickstart.bat      # Windows quickstart script
│   └── quickstart.sh       # Linux/Mac quickstart script
├── issues/                 # File-based issue tracking
│   ├── new/                # Newly reported issues
│   ├── wip/                # Work in progress
│   ├── done/               # Completed issues
│   ├── README.md
│   ├── KNOWN_ISSUES.md     # Common problems and solutions
│   └── ROADMAP.md          # Project roadmap
├── .env.example            # Example configuration
├── .gitignore
├── LICENSE
├── pyproject.toml          # Project metadata
├── requirements.txt        # Dependencies
└── README.md
```

## Inspiration

This project was inspired by [Nomoos/StoryGenerator](https://github.com/Nomoos/StoryGenerator) and adapted for idea collection and inspiration gathering.

## License

This project is proprietary software. See [LICENSE](LICENSE) file for details.

**All Rights Reserved** - Copyright (c) 2025 PrismQ

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details on:

- Code of Conduct
- How to report bugs
- How to suggest features
- Development setup
- Pull request process
- Coding standards

For quick reference:
- **Bug Reports**: Open an issue on GitHub
- **Feature Requests**: Open an issue on GitHub
- **Questions**: Start a [discussion](https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource/discussions)

## Troubleshooting

For detailed troubleshooting, see:
- [Known Issues](issues/KNOWN_ISSUES.md) - Common problems and solutions
- [Windows Quickstart Guide](docs/WINDOWS_QUICKSTART.md#troubleshooting) - Windows-specific help

### Quick Solutions

#### Windows-Specific Issues

- **Module not found**: Make sure you're running commands from the project root directory
- **Path issues**: Use forward slashes (/) or escaped backslashes (\\\\) in paths
- **API errors**: Verify your YouTube API key in the `.env` file

### Common Issues

- **No ideas scraped**: Check your YouTube API credentials and internet connection
- **Database locked**: Close any other processes accessing the database file
- **Rate limiting**: YouTube API has rate limits; reduce `YOUTUBE_MAX_RESULTS` value if needed

For more help, see the [full troubleshooting guide](issues/KNOWN_ISSUES.md).

## Support

For issues and questions, please open an issue on the GitHub repository.