#!/bin/bash
# PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource - Database Setup Script
# This script creates ideas.db in the user's working directory and sets up the youtube_shorts_source table
# Target: Linux (development support), Windows primary

echo "============================================================"
echo "PrismQ YouTube Shorts Source - Database Setup"
echo "============================================================"
echo

# Store the repository root (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set default Python executable
PYTHON_EXEC="python3"

# Check if Python executable exists
if ! command -v $PYTHON_EXEC &> /dev/null; then
    echo
    echo "[ERROR] Python executable '$PYTHON_EXEC' not found or not working."
    echo
    read -p "Please enter the Python executable path (e.g., python, python3): " PYTHON_INPUT
    
    PYTHON_EXEC="$PYTHON_INPUT"
    
    if ! command -v $PYTHON_EXEC &> /dev/null; then
        echo "[ERROR] Python executable '$PYTHON_EXEC' still not working."
        echo "[ERROR] Please install Python 3.8 or higher and try again."
        exit 1
    fi
fi

echo "[INFO] Using Python: $PYTHON_EXEC"
$PYTHON_EXEC --version
echo

# Find the nearest parent directory with "PrismQ" in its name
# This matches the behavior of config.py
PRISMQ_DIR=""
SEARCH_DIR="$(pwd)"

while [ "$SEARCH_DIR" != "/" ]; do
    # Check if current search directory contains "PrismQ" in its name
    if [[ "$(basename "$SEARCH_DIR")" == *"PrismQ"* ]]; then
        PRISMQ_DIR="$SEARCH_DIR"
        break
    fi
    # Move to parent directory
    SEARCH_DIR="$(dirname "$SEARCH_DIR")"
done

if [ -z "$PRISMQ_DIR" ]; then
    # No PrismQ directory found, use current directory as fallback
    USER_WORK_DIR="$(pwd)"
    echo "[INFO] No PrismQ directory found in path. Using current directory as working directory."
else
    # Found PrismQ directory, create working directory with _WD suffix
    PRISMQ_NAME="$(basename "$PRISMQ_DIR")"
    PRISMQ_PARENT="$(dirname "$PRISMQ_DIR")"
    USER_WORK_DIR="$PRISMQ_PARENT/${PRISMQ_NAME}_WD"
    
    echo "[INFO] Found PrismQ directory: $PRISMQ_DIR"
    echo "[INFO] Working directory (with _WD suffix): $USER_WORK_DIR"
fi

echo

# Create working directory if it doesn't exist
if [ ! -d "$USER_WORK_DIR" ]; then
    echo "[INFO] Creating working directory: $USER_WORK_DIR"
    mkdir -p "$USER_WORK_DIR"
fi

# Check if .env file exists in working directory, if not, create from example
WORK_DIR_ENV="$USER_WORK_DIR/.env"
if [ ! -f "$WORK_DIR_ENV" ]; then
    echo "[INFO] .env file not found in working directory."
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        echo "[INFO] Creating .env from .env.example..."
        cp "$SCRIPT_DIR/.env.example" "$WORK_DIR_ENV"
        echo "[INFO] .env file created in working directory."
    else
        echo "[INFO] Creating new .env file in working directory..."
        cat > "$WORK_DIR_ENV" << EOF
# Working Directory (automatically managed)
WORKING_DIRECTORY=$USER_WORK_DIR

# Database Configuration
DATABASE_PATH=db.s3db

# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_MAX_RESULTS=50

# YouTube Channel Configuration
YOUTUBE_CHANNEL_URL=
YOUTUBE_CHANNEL_MAX_SHORTS=10

# YouTube Trending Configuration
YOUTUBE_TRENDING_MAX_SHORTS=10

# YouTube Keyword Configuration
YOUTUBE_KEYWORD_MAX_SHORTS=10
EOF
        echo "[INFO] .env file created in working directory with default values."
    fi
    echo
fi

# Read DATABASE_PATH from .env in working directory if it exists
DB_PATH="db.s3db"
if [ -f "$WORK_DIR_ENV" ]; then
    DB_PATH=$(grep "^DATABASE_PATH=" "$WORK_DIR_ENV" | cut -d'=' -f2 | xargs)
    if [ -z "$DB_PATH" ]; then
        DB_PATH="db.s3db"
    fi
fi

# Create the full database path
FULL_DB_PATH="$USER_WORK_DIR/$DB_PATH"
echo "[INFO] .env location: $WORK_DIR_ENV"
echo "[INFO] Database will be created at: $FULL_DB_PATH"
echo

# Check if Python dependencies are installed
echo "[INFO] Checking Python dependencies..."
$PYTHON_EXEC -c "import sqlalchemy" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] SQLAlchemy not found. Installing dependencies..."
    $PYTHON_EXEC -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies."
        echo "[ERROR] Please run 'scripts/setup.sh' first to install all dependencies."
        exit 1
    fi
fi

# Use the init_db.py script to create the database
echo "[INFO] Creating database and youtube_shorts_source table..."
$PYTHON_EXEC scripts/init_db.py --db-path "$FULL_DB_PATH"

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Failed to create database or table."
    exit 1
fi

echo
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo
echo "Database Location: $FULL_DB_PATH"
echo "Table Created: youtube_shorts_source"
echo
echo "Table Schema:"
echo "  - id: INTEGER PRIMARY KEY AUTOINCREMENT"
echo "  - source: VARCHAR(100) NOT NULL (indexed)"
echo "  - source_id: VARCHAR(255) NOT NULL (indexed)"
echo "  - title: TEXT NOT NULL"
echo "  - description: TEXT"
echo "  - tags: TEXT (comma-separated)"
echo "  - score: FLOAT"
echo "  - score_dictionary: TEXT (JSON object with score components)"
echo "  - processed: BOOLEAN DEFAULT FALSE (indexed)"
echo "  - created_at: TIMESTAMP"
echo "  - updated_at: TIMESTAMP"
echo
echo "Indexes:"
echo "  - UNIQUE(source, source_id)"
echo "  - INDEX(score)"
echo "  - INDEX(created_at)"
echo "  - INDEX(processed)"
echo
echo "You can now use this database with PrismQ YouTube Shorts Source."
echo
echo "Next steps:"
echo "  1. Edit .env file to add your YouTube API key"
echo "  2. Run: python3 -m cli scrape"
echo "  3. View collected ideas: python3 -m cli list"
echo
