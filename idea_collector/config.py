"""Configuration management for PrismQ.IdeaCollector."""

import os
from pathlib import Path
from typing import Optional, List
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
        
        # YouTube configuration
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.youtube_max_results = int(os.getenv("YOUTUBE_MAX_RESULTS", "50"))
        
        # Reddit configuration
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
        self.reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "PrismQ.IdeaCollector/1.0")
        self.reddit_subreddits = self._parse_list(os.getenv("REDDIT_SUBREDDITS", "ideas"))
        self.reddit_limit = int(os.getenv("REDDIT_LIMIT", "100"))

    @staticmethod
    def _parse_list(value: str, delimiter: str = ",") -> List[str]:
        """Parse a comma-separated string into a list.
        
        Args:
            value: Comma-separated string
            delimiter: Delimiter character
            
        Returns:
            List of strings
        """
        return [item.strip() for item in value.split(delimiter) if item.strip()]
