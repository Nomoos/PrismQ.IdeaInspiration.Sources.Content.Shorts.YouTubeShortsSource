# PrismQ.IdeaCollector

PrismQ.IdeaCollector is a standalone Python CLI that gathers idea inspirations from multiple sources like YouTube Shorts and Reddit, normalizes them into a SQLite database, and scores them based on engagement metrics.

## Features

- **Multi-Source Scraping**: Extensible plugin architecture for scraping ideas from:
  - YouTube Shorts
  - Reddit (multiple subreddits)
  - Easy to add more sources
  
- **Smart Scoring**: Calculates scores based on engagement metrics with per-source weight customization
  
- **Deduplication**: Automatically prevents duplicate ideas using (source, source_id) unique constraint
  
- **SQLite Storage**: Stores ideas with complete metadata:
  - Title
  - Description
  - Tags
  - Score
  - Score dictionary (detailed scoring breakdown)
  - Source information
  
- **Simple Configuration**: Single `.env` file for all settings

- **Windows Compatible**: Designed to work seamlessly on Windows systems

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

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

# Scoring Configuration (comma-separated weights)
SCORING_YOUTUBE=1.0,0.8,0.6
SCORING_REDDIT=1.0,0.9,0.7
DEFAULT_SCORE_WEIGHTS=1.0,0.8,0.6
```

### Scoring Weights

The scoring system uses weighted components to calculate final scores:
- First weight: View/engagement score
- Second weight: Like/upvote score
- Third weight: Comment score
- Fourth weight (auto): Engagement rate

You can customize weights per source to prioritize different metrics.

### Universal Metrics for Cross-Platform Scoring

The scoring engine now supports **universal metrics** that can be used to score and compare content performance across platforms like YouTube, TikTok, Instagram Reels, and Podcasts.

#### Available Universal Metrics

1. **Engagement Rate (ER)**
   - Formula: `ER = (likes + comments + shares + saves) / views × 100%`
   - Measures how much viewers interact with content
   - Includes saves for complete engagement tracking

2. **Watch-Through/Completion Rate**
   - Formula: `Watch-Through % = (average watch time / video length) × 100%`
   - Normalizes performance across short-form and long-form content
   - Indicates content quality and retention

3. **Conversion Rate (CR)**
   - Formula: `CR = conversions / views × 100%`
   - Tracks business goals (subscribers, follows, clicks, signups)
   - Platform-agnostic metric for growth tracking

4. **Relative Performance Index (RPI)**
   - Formula: `RPI = (current metric / channel median) × 100%`
   - Compares content to creator's own average
   - Cancels out platform differences and channel size

5. **Universal Content Score (UCS)**
   - Combined formula: `UCS = 0.4 × ER + 0.4 × Watch-Through + 0.2 × RPI`
   - Single 0-100% score for cross-platform comparison
   - Balanced weighting of engagement, retention, and relative performance

#### Using Universal Metrics in Code

```python
from idea_collector.scoring import ScoringEngine

engine = ScoringEngine()

# Calculate individual metrics
metrics = {
    'views': 10000,
    'likes': 500,
    'comments': 50,
    'shares': 30,
    'saves': 20,
    'average_watch_time': 45,
    'video_length': 60,
    'channel_median_views': 8000,
    'conversions': 150
}

# Get engagement rate
er = engine.calculate_engagement_rate(metrics)  # Returns 6.0%

# Get watch-through rate
wtr = engine.calculate_watch_through_rate(metrics)  # Returns 75.0%

# Get conversion rate
cr = engine.calculate_conversion_rate(metrics)  # Returns 1.5%

# Get relative performance index
rpi = engine.calculate_relative_performance_index(metrics, 'views')  # Returns 125.0%

# Get all universal metrics together
scores = engine.calculate_universal_content_score(metrics)
# Returns:
# {
#     'universal_content_score': 52.4,
#     'engagement_rate': 6.0,
#     'watch_through_rate': 75.0,
#     'relative_performance_index': 125.0,
#     'conversion_rate': 1.5
# }
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
SCORING_TWITTER=1.0,0.8,0.6
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
│   ├── sources/
│   │   ├── __init__.py     # Base plugin interface
│   │   ├── reddit_plugin.py
│   │   └── youtube_plugin.py
│   └── scoring/
│       └── __init__.py     # Scoring engine
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_database.py
│   └── test_scoring.py
├── .env.example            # Example configuration
├── .gitignore
├── pyproject.toml          # Project metadata
├── requirements.txt        # Dependencies
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