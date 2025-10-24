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

# Find the topmost/root parent directory with "PrismQ" in its name
# This matches the behavior of config.py - continues searching to find the highest-level PrismQ directory
PRISMQ_DIR=""
SEARCH_DIR="$(pwd)"

while [ "$SEARCH_DIR" != "/" ]; do
    # Check if current search directory contains "PrismQ" in its name
    if [[ "$(basename "$SEARCH_DIR")" == *"PrismQ"* ]]; then
        # Found a PrismQ directory, but keep searching for higher-level ones
        PRISMQ_DIR="$SEARCH_DIR"
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

# Check if .env file exists in PrismQ directory (not working directory)
if [ -n "$PRISMQ_DIR" ]; then
    PRISMQ_ENV="$PRISMQ_DIR/.env"
else
    PRISMQ_ENV="$(pwd)/.env"
fi

if [ ! -f "$PRISMQ_ENV" ]; then
    echo "[INFO] .env file not found in PrismQ directory."
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        echo "[INFO] Creating .env from .env.example..."
        cp "$SCRIPT_DIR/.env.example" "$PRISMQ_ENV"
        echo "[INFO] .env file created in PrismQ directory."
    else
        echo "[INFO] Creating new .env file in PrismQ directory..."
        cat > "$PRISMQ_ENV" << EOF
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
        echo "[INFO] .env file created in PrismQ directory with default values."
    fi
    echo
fi

# Read WORKING_DIRECTORY from .env if it exists
ENV_WORK_DIR=$(grep "^WORKING_DIRECTORY=" "$PRISMQ_ENV" 2>/dev/null | cut -d'=' -f2 | xargs)

# If WORKING_DIRECTORY is not set in .env, ask user interactively
if [ -z "$ENV_WORK_DIR" ]; then
    echo "[INFO] WORKING_DIRECTORY not found in .env file."
    echo "[INFO] Default working directory: $USER_WORK_DIR"
    read -p "Use default working directory '$USER_WORK_DIR'? (Y/N): " CONFIRM_WORK_DIR
    
    if [[ "$CONFIRM_WORK_DIR" =~ ^[Yy]$ ]]; then
        ENV_WORK_DIR="$USER_WORK_DIR"
        echo "[INFO] Adding WORKING_DIRECTORY to .env file..."
        # Update or add WORKING_DIRECTORY in .env
        if grep -q "^WORKING_DIRECTORY=" "$PRISMQ_ENV" 2>/dev/null; then
            sed -i "s|^WORKING_DIRECTORY=.*|WORKING_DIRECTORY=$USER_WORK_DIR|" "$PRISMQ_ENV"
        else
            echo "WORKING_DIRECTORY=$USER_WORK_DIR" >> "$PRISMQ_ENV"
        fi
    else
        echo
        read -p "Enter the working directory path: " CUSTOM_WORK_DIR
        ENV_WORK_DIR="$CUSTOM_WORK_DIR"
        echo "[INFO] Adding WORKING_DIRECTORY to .env file..."
        # Update or add WORKING_DIRECTORY in .env
        if grep -q "^WORKING_DIRECTORY=" "$PRISMQ_ENV" 2>/dev/null; then
            sed -i "s|^WORKING_DIRECTORY=.*|WORKING_DIRECTORY=$CUSTOM_WORK_DIR|" "$PRISMQ_ENV"
        else
            echo "WORKING_DIRECTORY=$CUSTOM_WORK_DIR" >> "$PRISMQ_ENV"
        fi
    fi
    echo
fi

# Use WORKING_DIRECTORY from .env if it exists, otherwise use default
if [ -n "$ENV_WORK_DIR" ]; then
    USER_WORK_DIR="$ENV_WORK_DIR"
    echo "[INFO] Using working directory from .env: $USER_WORK_DIR"
fi

# Create working directory if it doesn't exist
if [ ! -d "$USER_WORK_DIR" ]; then
    echo "[INFO] Creating working directory: $USER_WORK_DIR"
    mkdir -p "$USER_WORK_DIR"
fi

# Read DATABASE_PATH from .env if it exists
DB_PATH="db.s3db"
if [ -f "$PRISMQ_ENV" ]; then
    DB_PATH=$(grep "^DATABASE_PATH=" "$PRISMQ_ENV" | cut -d'=' -f2 | xargs)
    if [ -z "$DB_PATH" ]; then
        DB_PATH="db.s3db"
    fi
fi

# Create the full database path
FULL_DB_PATH="$USER_WORK_DIR/$DB_PATH"
echo "[INFO] .env location: $PRISMQ_ENV"
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
