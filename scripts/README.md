# Setup and Quickstart Scripts

This folder contains installation and quickstart scripts for PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource.

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

#### `init_db.py`
Python script to initialize the database schema.

**Note**: This script requires the mod directory structure to be properly set up. If you encounter import errors, run the full setup scripts (`setup.sh` or `setup.bat`) first.

**Usage**:
```bash
# Default location (ideas.db)
python scripts/init_db.py

# Custom location
python scripts/init_db.py --db-path /path/to/custom.db

# Quiet mode (no output)
python scripts/init_db.py --quiet
```

**What it does**:
- Creates the SQLite database file
- Initializes the youtube_shorts_source table
- Sets up all necessary indexes
- Reports database statistics

### Database Setup Scripts

#### `setup_db.sh` (Linux/macOS)
Database initialization script for Unix-based systems.

**Usage**:
```bash
chmod +x setup_db.sh
./setup_db.sh
```

**What it does**:
- Creates .env file if it doesn't exist
- Checks Python installation
- Installs SQLAlchemy if needed
- Creates the database at the specified location
- Sets up the youtube_shorts_source table with all indexes

#### `setup_db.bat` (Windows)
Database initialization script for Windows.

**Usage**:
```cmd
setup_db.bat
```

**What it does**:
- Creates .env file if it doesn't exist
- Checks Python installation
- Installs SQLAlchemy if needed
- Creates the database at the specified location
- Sets up the youtube_shorts_source table with all indexes
- Provides detailed schema information

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

# 2. Initialize database (optional - can also run ./setup_db.sh from project root)
python scripts/init_db.py

# 3. Configure .env file with your YouTube API key
nano .env

# 4. Run quickstart
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

### Windows
```cmd
REM 1. Run setup
scripts\setup.bat

REM 2. Initialize database (optional - can also run setup_db.bat from project root)
python scripts\init_db.py

REM 3. Configure .env file with your YouTube API key
notepad .env

REM 4. Run quickstart
scripts\quickstart.bat
```

### Alternative: Database-Only Setup

If you only need to set up the database without installing all dependencies:

#### Linux/macOS
```bash
chmod +x setup_db.sh
./setup_db.sh
```

#### Windows
```cmd
setup_db.bat
```

These scripts will:
- Create the .env file if needed
- Check for Python and SQLAlchemy
- Initialize the database at your chosen location
- Display the complete database schema

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
