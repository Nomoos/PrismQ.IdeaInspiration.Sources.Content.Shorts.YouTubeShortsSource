# Quick Start Guide for Windows

This guide will help you get PrismQ.IdeaCollector up and running on Windows.

## Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **API Credentials** (you'll need these later):
   - **YouTube Data API v3 Key**: 
     - Go to [Google Cloud Console](https://console.cloud.google.com/)
     - Create a new project or select an existing one
     - Enable "YouTube Data API v3"
     - Create credentials (API Key)
   
   - **Reddit API Credentials**:
     - Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
     - Click "Create App" or "Create Another App"
     - Choose "script" as the app type
     - Note your client_id and client_secret

## Installation Steps

### 1. Open Command Prompt or PowerShell

Press `Win + R`, type `cmd`, and press Enter.

### 2. Navigate to the Project Directory

```cmd
cd C:\path\to\PrismQ.IdeaCollector
```

### 3. Run the Setup Script

```cmd
setup.bat
```

This will:
- Check if Python is installed
- Install all required dependencies
- Create a `.env` file from `.env.example`

### 4. Configure Your API Keys

Open the `.env` file in Notepad or your preferred text editor:

```cmd
notepad .env
```

Update the following values with your API credentials:

```ini
YOUTUBE_API_KEY=your_youtube_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

Save and close the file.

## Using the CLI

### Scrape Ideas

Scrape from all sources (YouTube and Reddit):
```cmd
python -m idea_collector.cli scrape
```

Scrape from Reddit only:
```cmd
python -m idea_collector.cli scrape --source reddit
```

Scrape from YouTube only:
```cmd
python -m idea_collector.cli scrape --source youtube
```

### View Collected Ideas

List top 20 ideas:
```cmd
python -m idea_collector.cli list
```

List top 50 ideas:
```cmd
python -m idea_collector.cli list --limit 50
```

View only Reddit ideas:
```cmd
python -m idea_collector.cli list --source reddit
```

### View Statistics

```cmd
python -m idea_collector.cli stats
```

### Clear All Ideas

```cmd
python -m idea_collector.cli clear
```

## Configuration Options

Edit `.env` to customize:

- **Database location**: Change `DATABASE_PATH`
- **Reddit subreddits**: Modify `REDDIT_SUBREDDITS` (comma-separated)
- **Scoring weights**: Adjust `SCORING_YOUTUBE` and `SCORING_REDDIT`
- **Results limit**: Change `YOUTUBE_MAX_RESULTS` and `REDDIT_LIMIT`

Example:
```ini
REDDIT_SUBREDDITS=startups,business,ideas,entrepreneur
YOUTUBE_MAX_RESULTS=100
REDDIT_LIMIT=200
```

## Troubleshooting

### "Python is not recognized..."

Python is not in your PATH. Either:
- Reinstall Python and check "Add Python to PATH" during installation
- Or manually add Python to your PATH in System Environment Variables

### "No module named 'idea_collector'"

Make sure you're running commands from the project root directory where `idea_collector` folder exists.

### "API Error" or "No ideas scraped"

- Check that your API credentials in `.env` are correct
- Ensure you have internet connection
- Verify your API quotas haven't been exceeded

### Database is Locked

Close any programs that might be accessing the database file (`ideas.db`).

## Tips

1. **Start Small**: Begin with small limits (e.g., `REDDIT_LIMIT=10`) to test your setup
2. **API Quotas**: Be aware of API rate limits - YouTube allows 10,000 units/day
3. **Backup**: The database is stored in `ideas.db` - back it up regularly if needed
4. **Custom Sources**: You can extend the tool by creating new source plugins

## Getting Help

For more detailed information, see the main `README.md` file.

For issues and questions, please open an issue on the GitHub repository.

## Next Steps

Once you've collected some ideas:

1. Review them using `python -m idea_collector.cli list`
2. Check the SQLite database directly using tools like [DB Browser for SQLite](https://sqlitebrowser.org/)
3. Export ideas for further analysis
4. Customize scoring weights to match your preferences

Happy idea collecting! 🚀
