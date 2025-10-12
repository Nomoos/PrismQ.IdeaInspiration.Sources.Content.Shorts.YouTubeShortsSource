# Setup and Quickstart Scripts

This folder contains installation and quickstart scripts for PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource.

## Available Scripts

### Setup Scripts

#### `setup.sh` (Linux/macOS)
Initial setup script for Unix-based systems.

**Usage**:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**What it does**:
- Checks Python installation
- Installs dependencies from requirements.txt
- Creates .env file from .env.example
- Optionally configures YouTube API credentials

#### `setup.bat` (Windows)
Initial setup script for Windows.

**Usage**:
```cmd
scripts\setup.bat
```

**What it does**:
- Checks Python installation
- Installs dependencies from requirements.txt
- Creates .env file from .env.example
- Guides through YouTube API configuration

### Quickstart Scripts

#### `quickstart.sh` (Linux/macOS)
Quick demonstration script for Unix-based systems.

**Usage**:
```bash
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

**What it does**:
- Verifies setup
- Runs a sample YouTube Shorts scraping session
- Displays collected ideas
- Shows statistics

#### `quickstart.bat` (Windows)
Quick demonstration script for Windows.

**Usage**:
```cmd
scripts\quickstart.bat
```

**What it does**:
- Verifies setup
- Runs a sample YouTube Shorts scraping session
- Displays collected ideas
- Shows statistics

## First Time Setup

### Linux/macOS
```bash
# 1. Run setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# 2. Configure .env file with your YouTube API key
nano .env

# 3. Run quickstart
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

### Windows
```cmd
REM 1. Run setup
scripts\setup.bat

REM 2. Configure .env file with your YouTube API key
notepad .env

REM 3. Run quickstart
scripts\quickstart.bat
```

## Manual Installation

If you prefer not to use scripts, see the [manual setup guide](../README.md#manual-setup) in the main README.

## Troubleshooting

### Script Permission Denied (Linux/macOS)
```bash
chmod +x scripts/*.sh
```

### Python Not Found
Ensure Python 3.8+ is installed and in your PATH:
```bash
python3 --version
```

### Dependency Installation Failed
Try installing dependencies manually:
```bash
pip install -r requirements.txt
```

## Getting Help

- See [main documentation](../README.md)
- Check [known issues](../issues/KNOWN_ISSUES.md)
- Visit [troubleshooting guide](../docs/WINDOWS_QUICKSTART.md#troubleshooting)
