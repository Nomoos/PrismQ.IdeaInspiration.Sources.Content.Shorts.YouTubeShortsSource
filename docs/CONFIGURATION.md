# Configuration Guide

This guide explains how the PrismQ YouTube Shorts Source manages configuration settings.

## Overview

The application uses a **local .env file** in your working directory to store configuration. Each working directory maintains its own independent configuration, allowing you to run the application from different locations with different settings.

## Working Directory Management

### Automatic Working Directory Detection

When you run the application, it automatically:

1. **Detects your current working directory** - Uses the directory where you run the command
2. **Creates a .env file if needed** - Automatically creates `.env` in your working directory if it doesn't exist
3. **Stores the working directory** - Saves `WORKING_DIRECTORY` in the `.env` file for reference
4. **Remembers your settings** - Configuration is persisted across multiple runs

### Example

```bash
# First run in a directory
cd /my/project/folder
youtube-shorts-source stats

# The application creates /my/project/folder/.env with:
# WORKING_DIRECTORY='/my/project/folder'
# DATABASE_PATH=db.s3db
# ... other settings ...

# Future runs in the same directory use the same .env
youtube-shorts-source scrape-trending --top 20
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
youtube-shorts-source scrape-channel --channel @example
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
youtube-shorts-source stats --no-interactive
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

## Multiple Working Directories

You can run the application from different directories with independent configurations:

```bash
# Project A
cd /projects/project-a
youtube-shorts-source scrape-trending --top 5
# Uses /projects/project-a/.env
# Database: /projects/project-a/db.s3db

# Project B
cd /projects/project-b
youtube-shorts-source scrape-trending --top 20
# Uses /projects/project-b/.env
# Database: /projects/project-b/db.s3db
```

Each directory maintains:
- Its own `.env` file
- Its own database file (unless you specify an absolute path)
- Its own configuration settings

## Custom .env File Location

Override the default `.env` location using the `--env-file` option:

```bash
youtube-shorts-source stats --env-file /path/to/custom.env
```

When you specify a custom `.env` file:
- The **working directory** is set to the parent directory of the `.env` file
- All relative paths are resolved from that directory

## Best Practices

### 1. One Directory Per Project

Create a dedicated directory for each project or use case:

```bash
mkdir youtube-trending-ideas
cd youtube-trending-ideas
youtube-shorts-source scrape-trending
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
youtube-shorts-source stats --no-interactive
```

## Advanced Usage

### Environment Variables Override

Environment variables take precedence over `.env` file values:

```bash
DATABASE_PATH=special.db youtube-shorts-source stats
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
