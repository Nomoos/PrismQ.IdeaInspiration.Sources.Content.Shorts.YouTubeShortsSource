@echo off
REM PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource - Database Setup Script
REM This script creates ideas.db in the user's working directory and sets up the youtube_shorts_source table
REM Target: Windows with NVIDIA RTX 5090, AMD Ryzen, 64GB RAM

setlocal enabledelayedexpansion

echo ============================================================
echo PrismQ YouTube Shorts Source - Database Setup
echo ============================================================
echo.

REM Store the repository root (where this script is located)
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Set default Python executable
set "PYTHON_EXEC=python"

REM Check if .env file exists, if not, create from example
if not exist ".env" (
    echo [INFO] .env file not found.
    if exist ".env.example" (
        echo [INFO] Creating .env from .env.example...
        copy ".env.example" ".env" >nul
        echo [INFO] .env file created.
    ) else (
        echo [INFO] Creating new .env file...
        (
            echo # Database Configuration
            echo DATABASE_PATH=ideas.db
            echo.
            echo # YouTube API Configuration
            echo YOUTUBE_API_KEY=your_youtube_api_key_here
            echo YOUTUBE_MAX_RESULTS=50
            echo.
            echo # YouTube Channel Configuration
            echo YOUTUBE_CHANNEL_URL=
            echo YOUTUBE_CHANNEL_MAX_SHORTS=10
            echo.
            echo # YouTube Trending Configuration
            echo YOUTUBE_TRENDING_MAX_SHORTS=10
            echo.
            echo # YouTube Keyword Configuration
            echo YOUTUBE_KEYWORD_MAX_SHORTS=10
        ) > ".env"
        echo [INFO] .env file created with default values.
    )
    echo.
)

REM Read DATABASE_PATH from .env if it exists
set "DB_PATH=ideas.db"
for /f "tokens=1,2 delims==" %%a in ('findstr /i "^DATABASE_PATH=" .env 2^>nul') do (
    set "DB_PATH=%%b"
)

REM Remove any leading/trailing spaces
set "DB_PATH=%DB_PATH: =%"

REM Check if Python executable exists
%PYTHON_EXEC% --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python executable '%PYTHON_EXEC%' not found or not working.
    echo.
    set /p "PYTHON_INPUT=Please enter the Python executable path (e.g., python, python3, C:\Python310\python.exe): "
    
    REM Update the user's input
    set "PYTHON_EXEC=!PYTHON_INPUT!"
    
    REM Test again
    !PYTHON_EXEC! --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python executable '!PYTHON_EXEC!' still not working.
        echo [ERROR] Please install Python 3.8 or higher and try again.
        pause
        exit /b 1
    )
)

echo [INFO] Using Python: %PYTHON_EXEC%
%PYTHON_EXEC% --version
echo.

REM Get the current working directory (where user called the script from)
set "USER_WORK_DIR=%CD%"
echo [INFO] Current working directory: %USER_WORK_DIR%
echo.

REM Ask user where to create the database
echo The database will be created in your current working directory.
set /p "CONFIRM=Create %DB_PATH% in '%USER_WORK_DIR%'? (Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo.
    set /p "CUSTOM_DIR=Enter the full path where you want to create %DB_PATH%: "
    set "USER_WORK_DIR=!CUSTOM_DIR!"
)

REM Create the full database path
set "FULL_DB_PATH=%USER_WORK_DIR%\%DB_PATH%"
echo.
echo [INFO] Database will be created at: %FULL_DB_PATH%
echo.

REM Check if Python dependencies are installed
echo [INFO] Checking Python dependencies...
%PYTHON_EXEC% -c "import sqlalchemy" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] SQLAlchemy not found. Installing dependencies...
    %PYTHON_EXEC% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        echo [ERROR] Please run 'scripts\setup.bat' first to install all dependencies.
        pause
        exit /b 1
    )
)

REM Use the init_db.py script to create the database
echo [INFO] Creating database and youtube_shorts_source table...
%PYTHON_EXEC% scripts\init_db.py --db-path "%FULL_DB_PATH%"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to create database or table.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Database Location: %FULL_DB_PATH%
echo Table Created: youtube_shorts_source
echo.
echo Table Schema:
echo   - id: INTEGER PRIMARY KEY AUTOINCREMENT
echo   - source: VARCHAR(100) NOT NULL (indexed)
echo   - source_id: VARCHAR(255) NOT NULL (indexed)
echo   - title: TEXT NOT NULL
echo   - description: TEXT
echo   - tags: TEXT (comma-separated)
echo   - score: FLOAT
echo   - score_dictionary: TEXT (JSON object with score components)
echo   - processed: BOOLEAN DEFAULT FALSE (indexed)
echo   - created_at: TIMESTAMP
echo   - updated_at: TIMESTAMP
echo.
echo Indexes:
echo   - UNIQUE(source, source_id)
echo   - INDEX(score)
echo   - INDEX(created_at)
echo   - INDEX(processed)
echo.
echo You can now use this database with PrismQ YouTube Shorts Source.
echo.
echo Next steps:
echo   1. Edit .env file to add your YouTube API key
echo   2. Run: python -m cli scrape
echo   3. View collected ideas: python -m cli list
echo.
pause
