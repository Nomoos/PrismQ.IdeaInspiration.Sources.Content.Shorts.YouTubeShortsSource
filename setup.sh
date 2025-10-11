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
    echo "IMPORTANT: Please edit the .env file and add your API credentials:"
    echo "  - YOUTUBE_API_KEY"
    echo "  - REDDIT_CLIENT_ID"
    echo "  - REDDIT_CLIENT_SECRET"
    echo
else
    echo ".env file already exists."
    echo
fi

echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "To get started:"
echo "  1. Edit .env file with your API credentials"
echo "  2. Run: python3 -m idea_collector.cli scrape"
echo "  3. View ideas: python3 -m idea_collector.cli list"
echo
echo "For help: python3 -m idea_collector.cli --help"
echo
