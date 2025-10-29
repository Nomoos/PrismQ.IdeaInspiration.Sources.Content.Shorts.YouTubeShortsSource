@echo off
REM Quickstart script for PrismQ.IdeaCollector on Windows
REM Supports interactive mode when .env file is not present

echo ========================================
echo PrismQ.IdeaCollector - Quickstart
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo No .env file found. Starting interactive configuration...
    echo.
    
    REM Create .env file from .env.example if it exists
    if exist .env.example (
        copy .env.example .env >nul
    ) else (
        echo Creating new .env file...
        (
            echo # Database Configuration
            echo DATABASE_PATH=ideas.db
            echo.
            echo # YouTube Configuration
            echo YOUTUBE_API_KEY=
            echo YOUTUBE_MAX_RESULTS=50
            echo.
            echo # Reddit Configuration
            echo REDDIT_CLIENT_ID=
            echo REDDIT_CLIENT_SECRET=
            echo REDDIT_USER_AGENT=PrismQ.IdeaCollector/1.0
            echo REDDIT_SUBREDDITS=ideas,startup_ideas,SomebodyMakeThis
            echo REDDIT_LIMIT=100
        ) > .env
    )
    
    echo .env file created!
    echo.
    echo ========================================
    echo Interactive Configuration
    echo ========================================
    echo.
    echo Please provide your API credentials:
    echo (Press Enter to skip if you don't have the credentials yet)
    echo.
    
    REM Prompt for YouTube API Key
    set /p YOUTUBE_KEY="YouTube API Key: "
    
    REM Prompt for Reddit credentials
    set /p REDDIT_ID="Reddit Client ID: "
    set /p REDDIT_SECRET="Reddit Client Secret: "
    
    echo.
    echo Updating .env file...
    
    REM Update .env file with provided values
    REM Use PowerShell for more robust string replacement
    if not "%YOUTUBE_KEY%"=="" (
        powershell -Command "$key = '%YOUTUBE_KEY%'; (Get-Content .env) -replace 'YOUTUBE_API_KEY=.*', \"YOUTUBE_API_KEY=$key\" | Set-Content .env"
    )
    if not "%REDDIT_ID%"=="" (
        powershell -Command "$id = '%REDDIT_ID%'; (Get-Content .env) -replace 'REDDIT_CLIENT_ID=.*', \"REDDIT_CLIENT_ID=$id\" | Set-Content .env"
    )
    if not "%REDDIT_SECRET%"=="" (
        powershell -Command "$secret = '%REDDIT_SECRET%'; (Get-Content .env) -replace 'REDDIT_CLIENT_SECRET=.*', \"REDDIT_CLIENT_SECRET=$secret\" | Set-Content .env"
    )
    
    echo Configuration saved to .env
    echo.
    echo You can edit the .env file manually at any time to update your credentials.
    echo.
)

echo ========================================
echo Starting Data Collection
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run setup.bat first to install dependencies
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import click" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found. Installing...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Choose an option:
echo   1. Scrape from all sources
echo   2. Scrape from Reddit only
echo   3. Scrape from YouTube only
echo   4. List collected ideas
echo   5. Show statistics
echo   6. Exit
echo.

set /p CHOICE="Enter your choice (1-6): "

if "%CHOICE%"=="1" (
    echo.
    echo Scraping from all sources...
    python -m src.cli scrape
) else (
    if "%CHOICE%"=="2" (
        echo.
        echo Scraping from Reddit...
        python -m src.cli scrape --source reddit
    ) else (
        if "%CHOICE%"=="3" (
            echo.
            echo Scraping from YouTube...
            python -m src.cli scrape --source youtube
        ) else (
            if "%CHOICE%"=="4" (
                echo.
                echo Listing collected ideas...
                python -m src.cli list
            ) else (
                if "%CHOICE%"=="5" (
                    echo.
                    echo Showing statistics...
                    python -m src.cli stats
                ) else (
                    if "%CHOICE%"=="6" (
                        echo.
                        echo Exiting...
                        exit /b 0
                    ) else (
                        echo.
                        echo Invalid choice. Exiting...
                        exit /b 1
                    )
                )
            )
        )
    )
)

echo.
echo ========================================
echo Operation completed!
echo ========================================
echo.

pause
