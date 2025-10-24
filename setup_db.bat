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

REM Find the topmost/root parent directory with "PrismQ" in its name
REM Strategy: Search upward from current directory to root, updating PRISMQ_DIR each time
REM we find a directory with "PrismQ" in its name. Since we search upward (child -> parent),
REM the last match found will be the topmost/root PrismQ directory.
set "PRISMQ_DIR="
set "SEARCH_DIR=%CD%"

:search_prismq
REM Check if current search directory contains "PrismQ" in its name
echo %SEARCH_DIR% | findstr /i "PrismQ" >nul
if not errorlevel 1 (
    REM Found a PrismQ directory - save it and keep searching upward
    REM As we continue upward, we'll overwrite this if we find a higher-level PrismQ directory
    set "PRISMQ_DIR=%SEARCH_DIR%"
)

REM Move to parent directory
for %%i in ("%SEARCH_DIR%\..") do set "PARENT_DIR=%%~fi"

REM Check if we've reached the root (parent is same as current)
if "%SEARCH_DIR%"=="%PARENT_DIR%" goto search_complete

REM Continue searching in parent
set "SEARCH_DIR=%PARENT_DIR%"
goto search_prismq

:search_complete
REM At this point, PRISMQ_DIR contains the topmost PrismQ directory (or is empty if none found)
if "%PRISMQ_DIR%"=="" goto no_prismq_found
goto found_prismq

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

REM Check if .env file exists in PrismQ directory (not working directory)
set "PRISMQ_ENV=%PRISMQ_DIR%\.env"
if "%PRISMQ_DIR%"=="" set "PRISMQ_ENV=%CD%\.env"

if not exist "%PRISMQ_ENV%" (
    echo [INFO] .env file not found in PrismQ directory.
    if exist "%SCRIPT_DIR%.env.example" (
        echo [INFO] Creating .env from .env.example...
        copy "%SCRIPT_DIR%.env.example" "%PRISMQ_ENV%" >nul
        echo [INFO] .env file created in PrismQ directory.
    ) else (
        echo [INFO] Creating new .env file in PrismQ directory...
        (
            echo # Working Directory (automatically managed)
            echo WORKING_DIRECTORY=%USER_WORK_DIR%
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
        ) > "%PRISMQ_ENV%"
        echo [INFO] .env file created in PrismQ directory with default values.
    )
    echo.
)

REM Read WORKING_DIRECTORY from .env if it exists
set "ENV_WORK_DIR="
for /f "tokens=1,2 delims==" %%a in ('findstr /i "^WORKING_DIRECTORY=" "%PRISMQ_ENV%" 2^>nul') do (
    set "ENV_WORK_DIR=%%b"
)

REM Remove any leading/trailing spaces and quotes
set "ENV_WORK_DIR=%ENV_WORK_DIR: =%"
set "ENV_WORK_DIR=%ENV_WORK_DIR:"=%"

REM If WORKING_DIRECTORY is not set in .env, ask user interactively
if "%ENV_WORK_DIR%"=="" (
    echo [INFO] WORKING_DIRECTORY not found in .env file.
    echo [INFO] Default working directory: %USER_WORK_DIR%
    set /p "CONFIRM_WORK_DIR=Use default working directory '%USER_WORK_DIR%'? (Y/N): "
    
    if /i "!CONFIRM_WORK_DIR!"=="Y" (
        set "ENV_WORK_DIR=%USER_WORK_DIR%"
        echo [INFO] Adding WORKING_DIRECTORY to .env file...
        REM Add WORKING_DIRECTORY to .env
        powershell -Command "(Get-Content '%PRISMQ_ENV%') -replace '^WORKING_DIRECTORY=.*$', 'WORKING_DIRECTORY=%USER_WORK_DIR%' | Set-Content '%PRISMQ_ENV%'" 2>nul || (
            echo # Working Directory (automatically managed) >> "%PRISMQ_ENV%"
            echo WORKING_DIRECTORY=%USER_WORK_DIR% >> "%PRISMQ_ENV%"
        )
    ) else (
        echo.
        set /p "CUSTOM_WORK_DIR=Enter the working directory path: "
        set "ENV_WORK_DIR=!CUSTOM_WORK_DIR!"
        echo [INFO] Adding WORKING_DIRECTORY to .env file...
        REM Add WORKING_DIRECTORY to .env
        powershell -Command "(Get-Content '%PRISMQ_ENV%') -replace '^WORKING_DIRECTORY=.*$', 'WORKING_DIRECTORY=!CUSTOM_WORK_DIR!' | Set-Content '%PRISMQ_ENV%'" 2>nul || (
            echo # Working Directory (automatically managed) >> "%PRISMQ_ENV%"
            echo WORKING_DIRECTORY=!CUSTOM_WORK_DIR! >> "%PRISMQ_ENV%"
        )
    )
    echo.
)

REM Use WORKING_DIRECTORY from .env if it exists, otherwise use default
if not "%ENV_WORK_DIR%"=="" (
    set "USER_WORK_DIR=%ENV_WORK_DIR%"
    echo [INFO] Using working directory from .env: !USER_WORK_DIR!
)

REM Create working directory if it doesn't exist
if not exist "%USER_WORK_DIR%" (
    echo [INFO] Creating working directory: %USER_WORK_DIR%
    mkdir "%USER_WORK_DIR%"
)

REM Read DATABASE_PATH from .env if it exists
set "DB_PATH=db.s3db"
for /f "tokens=1,2 delims==" %%a in ('findstr /i "^DATABASE_PATH=" "%PRISMQ_ENV%" 2^>nul') do (
    set "DB_PATH=%%b"
)

REM Remove any leading/trailing spaces
set "DB_PATH=%DB_PATH: =%"

REM Create the full database path
set "FULL_DB_PATH=%USER_WORK_DIR%\%DB_PATH%"
echo [INFO] .env location: %PRISMQ_ENV%
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
