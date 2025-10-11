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
        
        # Scoring configuration
        self.scoring_youtube = self._parse_floats(os.getenv("SCORING_YOUTUBE", "1.0,0.8,0.6"))
        self.scoring_reddit = self._parse_floats(os.getenv("SCORING_REDDIT", "1.0,0.9,0.7"))
        self.default_score_weights = self._parse_floats(os.getenv("DEFAULT_SCORE_WEIGHTS", "1.0,0.8,0.6"))

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

    @staticmethod
    def _parse_floats(value: str, delimiter: str = ",") -> List[float]:
        """Parse a comma-separated string into a list of floats.
        
        Args:
            value: Comma-separated string of numbers
            delimiter: Delimiter character
            
        Returns:
            List of floats
        """
        try:
            return [float(item.strip()) for item in value.split(delimiter) if item.strip()]
        except ValueError:
            return [1.0]

    def get_source_weights(self, source: str) -> List[float]:
        """Get scoring weights for a specific source.
        
        Args:
            source: Source name (e.g., 'youtube', 'reddit')
            
        Returns:
            List of weight values
        """
        source_lower = source.lower()
        if source_lower == "youtube":
            return self.scoring_youtube
        elif source_lower == "reddit":
            return self.scoring_reddit
        else:
            return self.default_score_weights
