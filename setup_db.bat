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
            echo # Working Directory (automatically managed)
            echo WORKING_DIRECTORY=
            echo.
            echo # Database Configuration
            echo DATABASE_PATH=db.s3db
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
set "DB_PATH=db.s3db"
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

REM Find the nearest parent directory with "PrismQ" in its name
REM This matches the behavior of config.py
set "PRISMQ_DIR="
set "SEARCH_DIR=%CD%"

:search_prismq
REM Check if current search directory contains "PrismQ" in its name
echo %SEARCH_DIR% | findstr /i "PrismQ" >nul
if not errorlevel 1 (
    set "PRISMQ_DIR=%SEARCH_DIR%"
    goto found_prismq
)

REM Move to parent directory
for %%i in ("%SEARCH_DIR%\..") do set "PARENT_DIR=%%~fi"

REM Check if we've reached the root (parent is same as current)
if "%SEARCH_DIR%"=="%PARENT_DIR%" goto no_prismq_found

REM Continue searching in parent
set "SEARCH_DIR=%PARENT_DIR%"
goto search_prismq

:no_prismq_found
REM No PrismQ directory found, use current directory as fallback
set "USER_WORK_DIR=%CD%"
echo [INFO] No PrismQ directory found in path. Using current directory as working directory.
goto setup_db_path

:found_prismq
REM Found PrismQ directory, create working directory with _WD suffix
for %%i in ("%PRISMQ_DIR%") do set "PRISMQ_NAME=%%~nxi"
for %%i in ("%PRISMQ_DIR%\..") do set "PRISMQ_PARENT=%%~fi"
set "USER_WORK_DIR=%PRISMQ_PARENT%\%PRISMQ_NAME%_WD"

echo [INFO] Found PrismQ directory: %PRISMQ_DIR%
echo [INFO] Working directory (with _WD suffix): %USER_WORK_DIR%

:setup_db_path
echo.

REM Create working directory if it doesn't exist
if not exist "%USER_WORK_DIR%" (
    echo [INFO] Creating working directory: %USER_WORK_DIR%
    mkdir "%USER_WORK_DIR%"
)

REM Create the full database path
set "FULL_DB_PATH=%USER_WORK_DIR%\%DB_PATH%"
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
