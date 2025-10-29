#!/bin/bash

# Quickstart script for PrismQ.IdeaCollector on Linux/Mac
# Supports interactive mode when .env file is not present

echo "========================================"
echo "PrismQ.IdeaCollector - Quickstart"
echo "========================================"
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "No .env file found. Starting interactive configuration..."
    echo
    
    # Create .env file from .env.example if it exists
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        echo "Creating new .env file..."
        cat > .env << EOF
# Database Configuration
DATABASE_PATH=ideas.db

# YouTube Configuration
YOUTUBE_API_KEY=
YOUTUBE_MAX_RESULTS=50

# Reddit Configuration
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=PrismQ.IdeaCollector/1.0
REDDIT_SUBREDDITS=ideas,startup_ideas,SomebodyMakeThis
REDDIT_LIMIT=100
EOF
    fi
    
    echo ".env file created!"
    echo
    echo "========================================"
    echo "Interactive Configuration"
    echo "========================================"
    echo
    echo "Please provide your API credentials:"
    echo "(Press Enter to skip if you don't have the credentials yet)"
    echo
    
    # Prompt for YouTube API Key
    read -p "YouTube API Key: " YOUTUBE_KEY
    
    # Prompt for Reddit credentials
    read -p "Reddit Client ID: " REDDIT_ID
    read -p "Reddit Client Secret: " REDDIT_SECRET
    
    echo
    echo "Updating .env file..."
    
    # Update .env file with provided values
    # Use a more robust sed approach to handle special characters
    if [ ! -z "$YOUTUBE_KEY" ]; then
        # Escape special characters in the value
        ESCAPED_KEY=$(printf '%s\n' "$YOUTUBE_KEY" | sed 's/[&/\]/\\&/g')
        sed -i.bak "s|YOUTUBE_API_KEY=.*|YOUTUBE_API_KEY=$ESCAPED_KEY|" .env
    fi
    if [ ! -z "$REDDIT_ID" ]; then
        ESCAPED_ID=$(printf '%s\n' "$REDDIT_ID" | sed 's/[&/\]/\\&/g')
        sed -i.bak "s|REDDIT_CLIENT_ID=.*|REDDIT_CLIENT_ID=$ESCAPED_ID|" .env
    fi
    if [ ! -z "$REDDIT_SECRET" ]; then
        ESCAPED_SECRET=$(printf '%s\n' "$REDDIT_SECRET" | sed 's/[&/\]/\\&/g')
        sed -i.bak "s|REDDIT_CLIENT_SECRET=.*|REDDIT_CLIENT_SECRET=$ESCAPED_SECRET|" .env
    fi
    
    # Remove backup files
    rm -f .env.bak
    
    echo "Configuration saved to .env"
    echo
    echo "You can edit the .env file manually at any time to update your credentials."
    echo
fi

echo "========================================"
echo "Starting Data Collection"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please run setup.sh first to install dependencies"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import click" &> /dev/null; then
    echo "Dependencies not found. Installing..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo
echo "Choose an option:"
echo "  1. Scrape from all sources"
echo "  2. Scrape from Reddit only"
echo "  3. Scrape from YouTube only"
echo "  4. List collected ideas"
echo "  5. Show statistics"
echo "  6. Exit"
echo

read -p "Enter your choice (1-6): " CHOICE

case $CHOICE in
    1)
        echo
        echo "Scraping from all sources..."
        python3 -m src.cli scrape
        ;;
    2)
        echo
        echo "Scraping from Reddit..."
        python3 -m src.cli scrape --source reddit
        ;;
    3)
        echo
        echo "Scraping from YouTube..."
        python3 -m src.cli scrape --source youtube
        ;;
    4)
        echo
        echo "Listing collected ideas..."
        python3 -m src.cli list
        ;;
    5)
        echo
        echo "Showing statistics..."
        python3 -m src.cli stats
        ;;
    6)
        echo
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo
echo "========================================"
echo "Operation completed!"
echo "========================================"
echo
