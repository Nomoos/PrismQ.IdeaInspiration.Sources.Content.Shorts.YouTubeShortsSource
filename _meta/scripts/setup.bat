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
    echo ========================================
    echo Interactive Configuration (Optional)
    echo ========================================
    echo.
    echo Would you like to configure API credentials now?
    echo (You can also edit .env file manually later)
    echo.
    set /p CONFIGURE="Configure now? (Y/N): "
    
    if /I "%CONFIGURE%"=="Y" (
        echo.
        echo Please provide your API credentials:
        echo (Press Enter to skip any field)
        echo.
        
        set /p YOUTUBE_KEY="YouTube API Key: "
        set /p REDDIT_ID="Reddit Client ID: "
        set /p REDDIT_SECRET="Reddit Client Secret: "
        
        echo.
        echo Updating .env file...
        
        if not "%YOUTUBE_KEY%"=="" (
            powershell -Command "$key = '%YOUTUBE_KEY%'; (Get-Content .env) -replace 'YOUTUBE_API_KEY=.*', \"YOUTUBE_API_KEY=$key\" | Set-Content .env"
        )
        if not "%REDDIT_ID%"=="" (
            powershell -Command "$id = '%REDDIT_ID%'; (Get-Content .env) -replace 'REDDIT_CLIENT_ID=.*', \"REDDIT_CLIENT_ID=$id\" | Set-Content .env"
        )
        if not "%REDDIT_SECRET%"=="" (
            powershell -Command "$secret = '%REDDIT_SECRET%'; (Get-Content .env) -replace 'REDDIT_CLIENT_SECRET=.*', \"REDDIT_CLIENT_SECRET=$secret\" | Set-Content .env"
        )
        
        echo Configuration saved!
        echo.
    ) else (
        echo.
        echo Skipping interactive configuration.
        echo IMPORTANT: Please edit the .env file and add your API credentials:
        echo   - YOUTUBE_API_KEY
        echo   - REDDIT_CLIENT_ID
        echo   - REDDIT_CLIENT_SECRET
        echo.
    )
) else (
    echo .env file already exists.
    echo.
)

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To get started:
echo   1. Run: quickstart.bat for interactive data collection
echo   2. Or manually run: python -m src.cli scrape
echo   3. View ideas: python -m src.cli list
echo.
echo For help: python -m src.cli --help
echo.

pause
