"""Tests for configuration module."""

import pytest
import tempfile
import os
from src.config import Config


@pytest.fixture
def temp_env_file():
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("DATABASE_PATH=test.db\n")
        f.write("YOUTUBE_API_KEY=test_key\n")
        f.write("YOUTUBE_MAX_RESULTS=25\n")
        f.write("REDDIT_CLIENT_ID=test_id\n")
        f.write("REDDIT_CLIENT_SECRET=test_secret\n")
        f.write("REDDIT_SUBREDDITS=test1,test2,test3\n")
        env_path = f.name
    
    yield env_path
    
    if os.path.exists(env_path):
        os.unlink(env_path)


def test_config_from_env_file(temp_env_file):
    """Test loading configuration from .env file."""
    config = Config(temp_env_file)
    
    assert config.database_path == "test.db"
    assert config.youtube_api_key == "test_key"
    assert config.youtube_max_results == 25
    assert config.reddit_client_id == "test_id"
    assert config.reddit_client_secret == "test_secret"
    assert config.reddit_subreddits == ["test1", "test2", "test3"]


def test_config_defaults():
    """Test configuration with default values."""
    # Clear environment variables to test defaults
    import os
    env_backup = {}
    env_vars = ['DATABASE_PATH', 'YOUTUBE_MAX_RESULTS', 'REDDIT_LIMIT']
    for var in env_vars:
        if var in os.environ:
            env_backup[var] = os.environ[var]
            del os.environ[var]
    
    try:
        # Create config without .env file
        config = Config("/nonexistent/.env")
        
        assert config.database_path == "ideas.db"
        assert config.youtube_max_results == 50
        assert config.reddit_limit == 100
    finally:
        # Restore environment variables
        for var, value in env_backup.items():
            os.environ[var] = value


def test_parse_list():
    """Test parsing comma-separated lists."""
    result = Config._parse_list("item1,item2, item3 , item4")
    assert result == ["item1", "item2", "item3", "item4"]
    
    result = Config._parse_list("")
    assert result == []
