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

- **YouTube Shorts Scraping**: Specialized scraper for YouTube Shorts videos
  - Filters for videos under 60 seconds
  - Extracts video metadata and statistics
  - Supports pagination and configurable result limits
  
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
  - Source information
  
- **Simple Configuration**: Single `.env` file for all settings

- **Interactive Mode**: Quickstart scripts with interactive configuration for easy setup

- **Windows Compatible**: Designed to work seamlessly on Windows systems

## Documentation

For comprehensive documentation, see:

- **[docs/](docs/)** - User and developer documentation
  - [Contributing Guidelines](docs/CONTRIBUTING.md)
  - [Metrics Documentation](docs/METRICS.md)
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

# YouTube Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_MAX_RESULTS=50
```

### Universal Metrics for Cross-Platform Scoring

The scoring engine now supports **universal metrics** that can be used to score and compare content performance across platforms like YouTube, TikTok, Instagram Reels, and Podcasts.

#### Available Universal Metrics

1. **Engagement Rate (ER)**
   - Formula: `ER = (likes + comments + shares + saves) / views × 100%`
   - Measures how much viewers interact with content
   - Includes saves for complete engagement tracking

2. **Watch-Through/Completion Rate**
   - Formula: `Watch-Through % = (average watch time / video length) × 100%`
   - Normalizes performance across short-form and long-form content
   - Indicates content quality and retention

3. **Conversion Rate (CR)**
   - Formula: `CR = conversions / views × 100%`
   - Tracks business goals (subscribers, follows, clicks, signups)
   - Platform-agnostic metric for growth tracking

4. **Relative Performance Index (RPI)**
   - Formula: `RPI = (current metric / channel median) × 100%`
   - Compares content to creator's own average
   - Cancels out platform differences and channel size

5. **Universal Content Score (UCS)**
   - Combined formula: `UCS = 0.4 × ER + 0.4 × Watch-Through + 0.2 × RPI`
   - Single 0-100% score for cross-platform comparison
   - Balanced weighting of engagement, retention, and relative performance

#### Using Universal Metrics in Code

```python
from src.scoring import ScoringEngine

engine = ScoringEngine()

# Calculate individual metrics
metrics = {
    'views': 10000,
    'likes': 500,
    'comments': 50,
    'shares': 30,
    'saves': 20,
    'average_watch_time': 45,
    'video_length': 60,
    'channel_median_views': 8000,
    'conversions': 150
}

# Get engagement rate
er = engine.calculate_engagement_rate(metrics)  # Returns 6.0%

# Get watch-through rate
wtr = engine.calculate_watch_through_rate(metrics)  # Returns 75.0%

# Get conversion rate
cr = engine.calculate_conversion_rate(metrics)  # Returns 1.5%

# Get relative performance index
rpi = engine.calculate_relative_performance_index(metrics, 'views')  # Returns 125.0%

# Get all universal metrics together
scores = engine.calculate_universal_content_score(metrics)
# Returns:
# {
#     'universal_content_score': 52.4,
#     'engagement_rate': 6.0,
#     'watch_through_rate': 75.0,
#     'relative_performance_index': 125.0,
#     'conversion_rate': 1.5
# }
```


## Usage

### Scrape Ideas

Scrape YouTube Shorts ideas:
```bash
python -m src.cli scrape
```

Use a custom .env file:
```bash
python -m src.cli scrape --env-file /path/to/.env
```

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