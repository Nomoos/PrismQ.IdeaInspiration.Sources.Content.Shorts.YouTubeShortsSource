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
        
        # YouTube configuration
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.youtube_max_results = int(os.getenv("YOUTUBE_MAX_RESULTS", "50"))
