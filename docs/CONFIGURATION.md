# Configuration Guide

This guide explains how the PrismQ YouTube Shorts Source manages configuration settings.

## Overview

The application uses a **local .env file** in your working directory to store configuration. Each working directory maintains its own independent configuration, allowing you to run the application from different locations with different settings.

## Working Directory Management

### Automatic Working Directory Detection

When you run the application, it automatically:

1. **Searches for PrismQ project directory** - Finds the nearest parent directory with "PrismQ" in its name
2. **Creates a .env file at project root** - Automatically creates `.env` in the PrismQ project directory
3. **Stores the working directory** - Saves `WORKING_DIRECTORY` in the `.env` file for reference
4. **Remembers your settings** - Configuration is persisted across multiple runs

### PrismQ Directory Search

The application searches upward from your current directory to find the nearest parent directory that contains "PrismQ" in its name. When found, it creates a separate working directory with the `_WD` suffix. This ensures that:

- All subdirectories within a PrismQ project share the same configuration
- You can run commands from anywhere within your project structure
- Configuration and databases are kept separate from the source code in a dedicated working directory
- The project root remains clean and focused on code

**Example directory structure:**
```
MyPrismQProject/              ← Source code repository
├── scripts/
│   └── processing/
│       └── run_here/         ← Run from here
└── data/

MyPrismQProject_WD/           ← Working directory (auto-created)
├── .env                      ← Configuration file
└── db.s3db                   ← Database file
```

If no directory with "PrismQ" in the name is found, the application falls back to using the current directory.

### Example

```bash
# First run in a PrismQ project subdirectory
cd /projects/MyPrismQProject/scripts/processing
python -m src.cli stats

# The application creates working directory with _WD suffix:
# /projects/MyPrismQProject_WD/.env with:
# WORKING_DIRECTORY='/projects/MyPrismQProject_WD'
# DATABASE_PATH=db.s3db
# ... other settings ...

# Future runs from any subdirectory use the same .env
cd /projects/MyPrismQProject/data
python -m src.cli scrape-trending --top 20
# Still uses /projects/MyPrismQProject_WD/.env
```

## Configuration Options

### Required Settings

None! All configuration settings have sensible defaults.

### Optional Settings

Configure these in your `.env` file or they'll use defaults:

| Setting | Default | Description |
|---------|---------|-------------|
| `WORKING_DIRECTORY` | (auto-detected) | Your working directory (automatically managed) |
| `DATABASE_PATH` | `db.s3db` | Path to SQLite database file |
| `YOUTUBE_API_KEY` | (empty) | YouTube API key for API-based scraping |
| `YOUTUBE_MAX_RESULTS` | `50` | Maximum results for YouTube API |
| `YOUTUBE_CHANNEL_URL` | (empty) | Default channel URL for scraping |
| `YOUTUBE_CHANNEL_MAX_SHORTS` | `10` | Maximum shorts to scrape from channel |
| `YOUTUBE_TRENDING_MAX_SHORTS` | `10` | Maximum shorts to scrape from trending |
| `YOUTUBE_KEYWORD_MAX_SHORTS` | `10` | Maximum shorts to scrape by keyword |

## Interactive vs Non-Interactive Mode

### Interactive Mode (Default)

In interactive mode, the application will:
- Prompt you for missing required values
- Save your responses to the `.env` file
- Use defaults for optional values if you don't provide them

**Example:**
```bash
python -m src.cli scrape-channel --channel @example
# If YOUTUBE_CHANNEL_MAX_SHORTS is not set, you might be prompted:
# Maximum shorts to scrape from channel (default: 10): 
```

### Non-Interactive Mode

Use the `--no-interactive` flag to:
- Skip all prompts
- Use default values for missing settings
- Useful for automation and CI/CD

**Example:**
```bash
python -m src.cli stats --no-interactive
```

## Configuration File Format

The `.env` file uses simple KEY=VALUE format:

```env
# Working Directory (automatically managed)
WORKING_DIRECTORY='/path/to/your/directory'

# Database Configuration
DATABASE_PATH=db.s3db

# YouTube API Configuration
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_MAX_RESULTS=50

# YouTube Channel Configuration
YOUTUBE_CHANNEL_URL=@channelname
YOUTUBE_CHANNEL_MAX_SHORTS=10

# YouTube Trending Configuration
YOUTUBE_TRENDING_MAX_SHORTS=10

# YouTube Keyword Configuration
YOUTUBE_KEYWORD_MAX_SHORTS=10
```

## Multiple PrismQ Projects

You can run the application from different PrismQ projects with independent configurations:

```bash
# Project A - Any subdirectory within ProjectA
cd /projects/MyPrismQProjectA/scripts
python -m src.cli scrape-trending --top 5
# Uses /projects/MyPrismQProjectA_WD/.env
# Database: /projects/MyPrismQProjectA_WD/db.s3db

# Project B - Any subdirectory within ProjectB
cd /projects/AnotherPrismQProjectB/data/processing
python -m src.cli scrape-trending --top 20
# Uses /projects/AnotherPrismQProjectB_WD/.env
# Database: /projects/AnotherPrismQProjectB_WD/db.s3db
```

Each PrismQ project maintains:
- Its own `.env` file at the project root
- Its own database file (unless you specify an absolute path)
- Its own configuration settings
- Shared configuration across all subdirectories within the project

## Custom .env File Location

Override the default `.env` location using the `--env-file` option:

```bash
python -m src.cli stats --env-file /path/to/custom.env
```

When you specify a custom `.env` file:
- The **working directory** is set to the parent directory of the `.env` file
- All relative paths are resolved from that directory

## Best Practices

### 1. Use PrismQ in Project Names

Create project directories with "PrismQ" in the name for automatic configuration management:

```bash
mkdir MyPrismQTrendingIdeas
cd MyPrismQTrendingIdeas
python -m src.cli scrape-trending

# Create subdirectories for organization
mkdir scripts data output
cd scripts
python -m src.cli scrape-channel --channel @example
# Still uses MyPrismQTrendingIdeas/.env
```

### 2. Version Control

**DO NOT** commit `.env` files to version control if they contain sensitive data like API keys.

Add to `.gitignore`:
```
.env
*.db
*.s3db
```

### 3. Use .env.example as Template

Copy the example file to create your own:

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Separate Databases

Use different databases for different purposes:

```env
# In /projects/testing/.env
DATABASE_PATH=test.db

# In /projects/production/.env
DATABASE_PATH=production.db
```

## Troubleshooting

### Problem: Configuration not persisting

**Solution:** Check file permissions on the `.env` file and directory.

```bash
ls -la .env
# Should be readable and writable by your user
```

### Problem: Different directory showing wrong config

**Solution:** Each directory needs its own `.env` file. Check which file is being used:

```bash
python -c "
from mod.config import Config
config = Config(interactive=False)
print(f'Env file: {config.env_file}')
print(f'Working directory: {config.working_directory}')
"
```

### Problem: Want to reset configuration

**Solution:** Simply delete the `.env` file and run the application again:

```bash
rm .env
python -m src.cli stats --no-interactive
```

## Advanced Usage

### Environment Variables Override

Environment variables take precedence over `.env` file values:

```bash
DATABASE_PATH=special.db python -m src.cli stats
```

### Programmatic Configuration

Use the Config class directly in your Python code:

```python
from mod.config import Config

# Load config from specific location
config = Config(env_file="/path/to/.env", interactive=False)

# Access configuration
print(config.database_path)
print(config.working_directory)
```

## See Also

- [README.md](../README.md) - Main documentation
- [.env.example](../.env.example) - Example configuration file
- [CLI Usage](../README.md#usage) - Command-line interface guide
