@echo off
REM Setup script for PrismQ.IdeaCollector on Windows

echo ========================================
echo PrismQ.IdeaCollector Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation successful!
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your API credentials:
    echo   - YOUTUBE_API_KEY
    echo   - REDDIT_CLIENT_ID
    echo   - REDDIT_CLIENT_SECRET
    echo.
) else (
    echo .env file already exists.
    echo.
)

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To get started:
echo   1. Edit .env file with your API credentials
echo   2. Run: python -m idea_collector.cli scrape
echo   3. View ideas: python -m idea_collector.cli list
echo.
echo For help: python -m idea_collector.cli --help
echo.

pause
