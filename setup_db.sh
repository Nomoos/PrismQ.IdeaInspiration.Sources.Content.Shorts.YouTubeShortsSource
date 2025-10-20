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

# Check if .env file exists, if not, create from example
if [ ! -f ".env" ]; then
    echo "[INFO] .env file not found."
    if [ -f ".env.example" ]; then
        echo "[INFO] Creating .env from .env.example..."
        cp ".env.example" ".env"
        echo "[INFO] .env file created."
    else
        echo "[INFO] Creating new .env file..."
        cat > ".env" << 'EOF'
# Database Configuration
DATABASE_PATH=ideas.db

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
        echo "[INFO] .env file created with default values."
    fi
    echo
fi

# Read DATABASE_PATH from .env if it exists
DB_PATH="ideas.db"
if [ -f ".env" ]; then
    DB_PATH=$(grep "^DATABASE_PATH=" .env | cut -d'=' -f2 | xargs)
    if [ -z "$DB_PATH" ]; then
        DB_PATH="ideas.db"
    fi
fi

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

# Get the current working directory (where user called the script from)
USER_WORK_DIR="$(pwd)"
echo "[INFO] Current working directory: $USER_WORK_DIR"
echo

# Ask user where to create the database
echo "The database will be created in your current working directory."
read -p "Create $DB_PATH in '$USER_WORK_DIR'? (Y/N): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo
    read -p "Enter the full path where you want to create $DB_PATH: " CUSTOM_DIR
    USER_WORK_DIR="$CUSTOM_DIR"
fi

# Create the full database path
FULL_DB_PATH="$USER_WORK_DIR/$DB_PATH"
echo
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
