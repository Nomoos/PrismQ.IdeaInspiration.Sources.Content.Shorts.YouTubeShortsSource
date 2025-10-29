#!/bin/bash

# Setup script for PrismQ.IdeaCollector on Linux/Mac

echo "========================================"
echo "PrismQ.IdeaCollector Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python found:"
python3 --version
echo

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "Installation successful!"
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo
    echo "========================================"
    echo "Interactive Configuration (Optional)"
    echo "========================================"
    echo
    echo "Would you like to configure API credentials now?"
    echo "(You can also edit .env file manually later)"
    echo
    read -p "Configure now? (Y/N): " CONFIGURE
    
    if [[ "$CONFIGURE" == "Y" || "$CONFIGURE" == "y" ]]; then
        echo
        echo "Please provide your API credentials:"
        echo "(Press Enter to skip any field)"
        echo
        
        read -p "YouTube API Key: " YOUTUBE_KEY
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
        
        echo "Configuration saved!"
        echo
    else
        echo
        echo "Skipping interactive configuration."
        echo "IMPORTANT: Please edit the .env file and add your API credentials:"
        echo "  - YOUTUBE_API_KEY"
        echo "  - REDDIT_CLIENT_ID"
        echo "  - REDDIT_CLIENT_SECRET"
        echo
    fi
else
    echo ".env file already exists."
    echo
fi

echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "To get started:"
echo "  1. Run: ./quickstart.sh for interactive data collection"
echo "  2. Or manually run: python3 -m src.cli scrape"
echo "  3. View ideas: python3 -m src.cli list"
echo
echo "For help: python3 -m src.cli --help"
echo
