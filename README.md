# PrismQ.IdeaCollector

PrismQ.IdeaCollector is a standalone Python CLI that gathers idea inspirations from multiple sources like YouTube Shorts and Reddit, and stores them in a SQLite database for later analysis.

## Features

- **Multi-Source Scraping**: Extensible plugin architecture for scraping ideas from:
  - YouTube Shorts
  - Reddit (multiple subreddits)
  - Easy to add more sources
  
- **Deduplication**: Automatically prevents duplicate ideas using (source, source_id) unique constraint
  
- **SQLite Storage**: Stores ideas with complete metadata:
  - Title
  - Description
  - Tags
  - Source information
  
- **Simple Configuration**: Single `.env` file for all settings

- **Interactive Mode**: Quickstart scripts with interactive configuration for easy setup

- **Windows Compatible**: Designed to work seamlessly on Windows systems

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start (Recommended)

#### Windows

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PrismQDev/PrismQ.IdeaCollector.git
   cd PrismQ.IdeaCollector
   ```

2. **Run setup**:
   ```batch
   setup.bat
   ```

3. **Run quickstart**:
   ```batch
   quickstart.bat
   ```

The quickstart script will guide you through:
- Interactive configuration (if no .env file exists)
- Choosing which sources to scrape
- Viewing collected ideas

#### Linux/Mac

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PrismQDev/PrismQ.IdeaCollector.git
   cd PrismQ.IdeaCollector
   ```

2. **Run setup**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Run quickstart**:
   ```bash
   chmod +x quickstart.sh
   ./quickstart.sh
   ```

### Manual Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PrismQDev/PrismQ.IdeaCollector.git
   cd PrismQ.IdeaCollector
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env  # On Windows
     # or
     cp .env.example .env    # On Linux/Mac
     ```
   
   - Edit `.env` and add your API credentials:
     - **YouTube API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/)
     - **Reddit API Credentials**: Get from [Reddit Apps](https://www.reddit.com/prefs/apps)

## Configuration

Edit the `.env` file to customize the application:

```ini
# Database Configuration
DATABASE_PATH=ideas.db

# YouTube Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_MAX_RESULTS=50

# Reddit Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PrismQ.IdeaCollector/1.0
REDDIT_SUBREDDITS=ideas,startup_ideas,SomebodyMakeThis
REDDIT_LIMIT=100
```

## Usage

### Scrape Ideas

Scrape ideas from all configured sources:
```bash
python -m idea_collector.cli scrape
```

Scrape from a specific source:
```bash
python -m idea_collector.cli scrape --source reddit
python -m idea_collector.cli scrape --source youtube
```

Use a custom .env file:
```bash
python -m idea_collector.cli scrape --env-file /path/to/.env
```

### List Ideas

List the top ideas (default: 20):
```bash
python -m idea_collector.cli list
```

Show more results:
```bash
python -m idea_collector.cli list --limit 50
```

Filter by source:
```bash
python -m idea_collector.cli list --source reddit
```

### View Statistics

View collection statistics:
```bash
python -m idea_collector.cli stats
```

### Clear Database

Clear all collected ideas:
```bash
python -m idea_collector.cli clear
```

## Database Schema

The SQLite database uses the following schema:

```sql
CREATE TABLE ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    score REAL,
    score_dictionary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, source_id)
);
```

## Extending with New Sources

To add a new source plugin:

1. Create a new file in `idea_collector/sources/` (e.g., `twitter_plugin.py`)

2. Implement the `SourcePlugin` interface:

```python
from idea_collector.sources import SourcePlugin

class TwitterPlugin(SourcePlugin):
    def get_source_name(self):
        return "twitter"
    
    def scrape(self):
        # Implement scraping logic
        ideas = []
        # ... scrape data ...
        return ideas
```

3. Add configuration to `.env`:
```ini
TWITTER_API_KEY=your_key
```

4. Import and use in `cli.py`

## Development

### Running Tests

Run the test suite:
```bash
pytest
```

With coverage:
```bash
pytest --cov=idea_collector --cov-report=html
```

### Project Structure

```
PrismQ.IdeaCollector/
├── idea_collector/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   └── sources/
│       ├── __init__.py     # Base plugin interface
│       ├── reddit_plugin.py
│       └── youtube_plugin.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_database.py
├── .env.example            # Example configuration
├── .gitignore
├── pyproject.toml          # Project metadata
├── requirements.txt        # Dependencies
├── setup.bat               # Windows setup script
├── setup.sh                # Linux/Mac setup script
├── quickstart.bat          # Windows quickstart script
├── quickstart.sh           # Linux/Mac quickstart script
└── README.md
```

## Inspiration

This project was inspired by [Nomoos/StoryGenerator](https://github.com/Nomoos/StoryGenerator) and adapted for idea collection and inspiration gathering.

## License

This project is open source and available for use and modification.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Troubleshooting

### Windows-Specific Issues

- **Module not found**: Make sure you're running commands from the project root directory
- **Path issues**: Use forward slashes (/) or escaped backslashes (\\\\) in paths
- **API errors**: Verify your API credentials in the `.env` file

### Common Issues

- **No ideas scraped**: Check your API credentials and internet connection
- **Database locked**: Close any other processes accessing the database file
- **Rate limiting**: YouTube and Reddit APIs have rate limits; reduce `MAX_RESULTS` and `LIMIT` values if needed

## Support

For issues and questions, please open an issue on the GitHub repository.