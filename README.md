# Business/Domain Modules (`mod/`)

This directory contains business logic and domain-specific modules for the PrismQ YouTube Shorts Source application.

## Purpose

The `mod/` directory holds higher-level modules that implement:
- YouTube content scraping plugins
- Database operations for idea storage
- Metrics tracking and analysis
- CLI interface for user interaction

## Separation of Concerns

The repository follows a clear separation:

- **`src/`** - Core Python package implementation (infrastructure)
  - Configuration management (`config.py`)
  - Logging infrastructure (`logging_config.py`)
  - Core utilities and common functionality
  - Package initialization

- **`mod/`** - Business/domain modules (this directory)
  - CLI interface (`cli.py`)
  - Database operations (`database.py`)
  - Universal metrics system (`metrics.py`)
  - YouTube scraping plugins (`sources/`)
    - `youtube_plugin.py` - YouTube API-based scraping
    - `youtube_channel_plugin.py` - Channel-based scraping with yt-dlp
    - `youtube_trending_plugin.py` - Trending and keyword-based scraping

## Structure

```
mod/
├── __init__.py                     # Module initialization
├── cli.py                          # Command-line interface
├── database.py                     # SQLite database operations
├── metrics.py                      # Universal metrics schema
└── sources/                        # Content source plugins
    ├── __init__.py                 # Source plugin base class
    ├── youtube_plugin.py           # YouTube API scraper
    ├── youtube_channel_plugin.py   # YouTube channel scraper
    └── youtube_trending_plugin.py  # Trending/keyword scraper
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
