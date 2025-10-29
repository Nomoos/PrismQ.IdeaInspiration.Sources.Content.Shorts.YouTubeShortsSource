# Business/Domain Modules (`mod/`)

This directory contains business logic and domain-specific modules for the PrismQ YouTube Shorts Source application.

## Purpose

The `mod/` directory holds higher-level modules that implement:
- Database operations for idea storage
- Metrics tracking and analysis
- YouTube content scraping plugins

## Separation of Concerns

The repository follows a clear separation:

- **Root Level** - Core implementation files
  - CLI interface (`cli.py`)
  - Configuration management (`config.py`)
  - Logging infrastructure (`logging_config.py`)
  - Database operations (`database.py`)
  - Universal metrics system (`metrics.py`)

- **`mod/`** - Business/domain modules (this directory)
  - Symlinks to some root-level files for module-style access
  - `config.py` -> symlink to ../config.py
  - `database.py` -> symlink to ../database.py
  - `metrics.py` -> symlink to ../metrics.py
  - `Model` -> symlink to ../Model (ORM model layer)
  - `sources` -> symlink to ../sources (YouTube scraping plugins)
    - `youtube_plugin.py` - YouTube API-based scraping
    - `youtube_channel_plugin.py` - Channel-based scraping with yt-dlp
    - `youtube_trending_plugin.py` - Trending and keyword-based scraping

## Structure

```
mod/
├── __init__.py                     # Module initialization
├── config.py -> ../config.py       # Symlink to configuration
├── database.py -> ../database.py   # Symlink to database operations
├── metrics.py -> ../metrics.py     # Symlink to metrics system
├── Model -> ../Model               # Symlink to ORM model layer
└── sources -> ../sources           # Symlink to source plugins
    ├── __init__.py                 # Source plugin base class
    ├── youtube_plugin.py           # YouTube API scraper
    ├── youtube_channel_plugin.py   # YouTube channel scraper
    └── youtube_trending_plugin.py  # Trending/keyword scraper
```

## Guidelines

When modifying modules:

1. **Single Responsibility**: Each module focuses on a specific concern
2. **File Location**: Edit the actual files at root level (symlinks point to them)
3. **Testing**: Update corresponding tests in `tests/`
4. **Documentation**: Keep docstrings and documentation up-to-date
5. **Code Quality**: Follow PEP 8 and use type hints

## Related Documentation

- Main README: `/README.md`
- Contributing Guidelines: `/docs/CONTRIBUTING.md`
- Copilot Instructions: `/.github/copilot-instructions.md`
