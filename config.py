"""Configuration management for PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource."""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv, set_key


class Config:
    """Manages application configuration from environment variables."""

    def __init__(self, env_file: Optional[str] = None, interactive: bool = True):
        """Initialize configuration.
        
        Args:
            env_file: Path to .env file (default: .env in nearest PrismQ directory)
            interactive: Whether to prompt for missing values (default: True)
        """
        # Determine working directory and .env file path
        if env_file is None:
            # Find nearest parent directory with "PrismQ" in its name
            prismq_dir = self._find_prismq_directory()
            self.working_directory = str(prismq_dir)
            env_file = prismq_dir / ".env"
        else:
            # Use the directory of the provided env_file as working directory
            env_path = Path(env_file)
            self.working_directory = str(env_path.parent.absolute())
            env_file = env_path
        
        self.env_file = str(env_file)
        self._interactive = interactive
        
        # Create .env file if it doesn't exist
        if not Path(self.env_file).exists():
            self._create_env_file()
        
        # Load environment variables from .env file
        load_dotenv(self.env_file)
        
        # Store/update working directory in .env
        self._ensure_working_directory()
        
        # Load configuration with interactive prompting for missing values
        self._load_configuration()
    
    def _find_prismq_directory(self) -> Path:
        """Find the nearest parent directory with 'PrismQ' in its name.
        
        Returns:
            Path to the nearest PrismQ directory, or current directory if none found
        """
        current_path = Path.cwd().absolute()
        
        # Check current directory and all parents
        for path in [current_path] + list(current_path.parents):
            if "PrismQ" in path.name:
                return path
        
        # If no PrismQ directory found, use current directory as fallback
        return current_path
    
    def _create_env_file(self):
        """Create a new .env file with default values."""
        Path(self.env_file).parent.mkdir(parents=True, exist_ok=True)
        Path(self.env_file).touch()
    
    def _ensure_working_directory(self):
        """Ensure working directory is stored in .env file."""
        current_wd = os.getenv("WORKING_DIRECTORY")
        
        if current_wd != self.working_directory:
            # Update or add working directory to .env
            set_key(self.env_file, "WORKING_DIRECTORY", self.working_directory)
            # Reload to pick up the change
            load_dotenv(self.env_file, override=True)
    
    def _prompt_for_value(self, key: str, description: str, default: str = "") -> str:
        """Prompt user for a configuration value.
        
        Args:
            key: Environment variable key
            description: Human-readable description of the value
            default: Default value to suggest
            
        Returns:
            The value entered by the user or the default
        """
        if not self._interactive:
            return default
        
        prompt = f"{description}"
        if default:
            prompt += f" (default: {default})"
        prompt += ": "
        
        try:
            value = input(prompt).strip()
            return value if value else default
        except (EOFError, KeyboardInterrupt):
            # In non-interactive environments, return default
            return default
    
    def _get_or_prompt(self, key: str, description: str, default: str = "", 
                      required: bool = False) -> str:
        """Get value from environment or prompt user if missing.
        
        Args:
            key: Environment variable key
            description: Human-readable description of the value
            default: Default value
            required: Whether this value is required
            
        Returns:
            The configuration value
        """
        value = os.getenv(key)
        
        if value is None or value == "":
            # Value is missing, prompt user if interactive
            if self._interactive and required:
                value = self._prompt_for_value(key, description, default)
                # Save the value to .env file
                if value:
                    set_key(self.env_file, key, value)
                    # Reload to pick up the change
                    load_dotenv(self.env_file, override=True)
            else:
                value = default
        
        return value
    
    def _load_configuration(self):
        """Load all configuration values with interactive prompting."""
        # Database configuration
        self.database_path = self._get_or_prompt(
            "DATABASE_PATH",
            "Database file path",
            "db.s3db",
            required=False
        )
        
        # YouTube API configuration (for search-based scraping)
        self.youtube_api_key = self._get_or_prompt(
            "YOUTUBE_API_KEY",
            "YouTube API key (optional, for API-based scraping)",
            "",
            required=False
        )
        
        youtube_max_results = self._get_or_prompt(
            "YOUTUBE_MAX_RESULTS",
            "Maximum results for YouTube API",
            "50",
            required=False
        )
        self.youtube_max_results = int(youtube_max_results) if youtube_max_results else 50
        
        # YouTube Channel configuration (for channel-based scraping with yt-dlp)
        self.youtube_channel_url = self._get_or_prompt(
            "YOUTUBE_CHANNEL_URL",
            "YouTube channel URL (optional)",
            "",
            required=False
        )
        
        youtube_channel_max_shorts = self._get_or_prompt(
            "YOUTUBE_CHANNEL_MAX_SHORTS",
            "Maximum shorts to scrape from channel",
            "10",
            required=False
        )
        self.youtube_channel_max_shorts = int(youtube_channel_max_shorts) if youtube_channel_max_shorts else 10
        
        # YouTube Trending configuration (for trending scraping with yt-dlp)
        youtube_trending_max_shorts = self._get_or_prompt(
            "YOUTUBE_TRENDING_MAX_SHORTS",
            "Maximum shorts to scrape from trending",
            "10",
            required=False
        )
        self.youtube_trending_max_shorts = int(youtube_trending_max_shorts) if youtube_trending_max_shorts else 10
        
        # YouTube Keyword configuration (for keyword search with yt-dlp)
        youtube_keyword_max_shorts = self._get_or_prompt(
            "YOUTUBE_KEYWORD_MAX_SHORTS",
            "Maximum shorts to scrape by keyword",
            "10",
            required=False
        )
        self.youtube_keyword_max_shorts = int(youtube_keyword_max_shorts) if youtube_keyword_max_shorts else 10
