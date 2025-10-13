"""Configuration management for PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Manages application configuration from environment variables."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            env_file: Path to .env file (default: .env in current directory)
        """
        if env_file is None:
            env_file = Path.cwd() / ".env"
        
        # Load environment variables from .env file
        if Path(env_file).exists():
            load_dotenv(env_file)
        
        # Database configuration
        self.database_path = os.getenv("DATABASE_PATH", "ideas.db")
        
        # YouTube API configuration (for search-based scraping)
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.youtube_max_results = int(os.getenv("YOUTUBE_MAX_RESULTS", "50"))
        
        # YouTube Channel configuration (for channel-based scraping with yt-dlp)
        self.youtube_channel_url = os.getenv("YOUTUBE_CHANNEL_URL", "")
        self.youtube_channel_max_shorts = int(os.getenv("YOUTUBE_CHANNEL_MAX_SHORTS", "10"))
        self.youtube_channel_story_only = os.getenv("YOUTUBE_CHANNEL_STORY_ONLY", "false").lower() == "true"
        
        # YouTube Trending configuration (for trending scraping with yt-dlp)
        self.youtube_trending_max_shorts = int(os.getenv("YOUTUBE_TRENDING_MAX_SHORTS", "10"))
        self.youtube_trending_story_only = os.getenv("YOUTUBE_TRENDING_STORY_ONLY", "false").lower() == "true"
        
        # YouTube Keyword configuration (for keyword search with yt-dlp)
        self.youtube_keyword_max_shorts = int(os.getenv("YOUTUBE_KEYWORD_MAX_SHORTS", "10"))
        self.youtube_keyword_story_only = os.getenv("YOUTUBE_KEYWORD_STORY_ONLY", "false").lower() == "true"
