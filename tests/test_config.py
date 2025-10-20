"""Tests for configuration module."""

import pytest
import tempfile
import os
from pathlib import Path
from mod.config import Config


@pytest.fixture
def temp_env_file():
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("DATABASE_PATH=test.db\n")
        f.write("YOUTUBE_API_KEY=test_key\n")
        f.write("YOUTUBE_MAX_RESULTS=25\n")
        env_path = f.name
    
    yield env_path
    
    if os.path.exists(env_path):
        os.unlink(env_path)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    import tempfile
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    import shutil
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


def test_config_from_env_file(temp_env_file):
    """Test loading configuration from .env file."""
    config = Config(temp_env_file, interactive=False)
    
    assert config.database_path == "test.db"
    assert config.youtube_api_key == "test_key"
    assert config.youtube_max_results == 25


def test_config_defaults():
    """Test configuration with default values."""
    # Clear environment variables to test defaults
    import os
    env_backup = {}
    env_vars = ['DATABASE_PATH', 'YOUTUBE_MAX_RESULTS', 'WORKING_DIRECTORY']
    for var in env_vars:
        if var in os.environ:
            env_backup[var] = os.environ[var]
            del os.environ[var]
    
    try:
        # Create config without .env file (non-interactive)
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            config = Config(str(env_path), interactive=False)
            
            assert config.database_path == "db.s3db"
            assert config.youtube_max_results == 50
    finally:
        # Restore environment variables
        for var, value in env_backup.items():
            os.environ[var] = value


def test_working_directory_stored(temp_dir):
    """Test that working directory is stored in .env file."""
    env_path = Path(temp_dir) / ".env"
    
    # Clear environment to avoid pollution
    env_backup = {}
    env_vars = ['DATABASE_PATH', 'YOUTUBE_MAX_RESULTS', 'WORKING_DIRECTORY']
    for var in env_vars:
        if var in os.environ:
            env_backup[var] = os.environ[var]
            del os.environ[var]
    
    try:
        # Create config
        config = Config(str(env_path), interactive=False)
        
        # Check that working directory is set
        assert config.working_directory == temp_dir
        
        # Check that it's stored in .env file
        assert env_path.exists()
        with open(env_path, 'r') as f:
            content = f.read()
            # The value might be quoted by set_key, so check for the value itself
            assert "WORKING_DIRECTORY=" in content
            assert temp_dir in content
    finally:
        # Restore environment variables
        for var, value in env_backup.items():
            os.environ[var] = value


def test_env_file_created_if_missing(temp_dir):
    """Test that .env file is created if it doesn't exist."""
    env_path = Path(temp_dir) / ".env"
    
    # Ensure file doesn't exist
    assert not env_path.exists()
    
    # Create config
    config = Config(str(env_path), interactive=False)
    
    # Check that file was created
    assert env_path.exists()
    assert config.env_file == str(env_path)


def test_working_directory_from_cwd(temp_dir):
    """Test that working directory defaults to current directory when no PrismQ dir found."""
    # Save original cwd
    original_cwd = os.getcwd()
    
    try:
        # Change to temp directory (no PrismQ in path)
        os.chdir(temp_dir)
        
        # Create config without specifying env_file
        config = Config(interactive=False)
        
        # Check that working directory is the temp directory (fallback)
        assert config.working_directory == temp_dir
        assert config.env_file == str(Path(temp_dir) / ".env")
    finally:
        # Restore original cwd
        os.chdir(original_cwd)


def test_working_directory_finds_prismq_parent():
    """Test that working directory finds nearest parent with PrismQ in name."""
    # Save original cwd
    original_cwd = os.getcwd()
    
    try:
        import tempfile
        import shutil
        
        # Create a temporary directory structure with PrismQ in the name
        base_temp = tempfile.mkdtemp()
        prismq_dir = Path(base_temp) / "MyPrismQProject"
        subdir = prismq_dir / "subdirectory" / "nested"
        subdir.mkdir(parents=True, exist_ok=True)
        
        # Change to nested subdirectory
        os.chdir(subdir)
        
        # Create config without specifying env_file
        config = Config(interactive=False)
        
        # Check that working directory is the PrismQ parent directory
        assert config.working_directory == str(prismq_dir)
        assert config.env_file == str(prismq_dir / ".env")
        assert (prismq_dir / ".env").exists()
        
        # Cleanup
        shutil.rmtree(base_temp)
    finally:
        # Restore original cwd
        os.chdir(original_cwd)


def test_working_directory_from_env_file_path(temp_dir):
    """Test that working directory is derived from env_file path."""
    env_path = Path(temp_dir) / "subdir" / ".env"
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create config
    config = Config(str(env_path), interactive=False)
    
    # Check that working directory is the parent of .env file
    assert config.working_directory == str(env_path.parent.absolute())


def test_config_non_interactive_mode(temp_dir):
    """Test that non-interactive mode doesn't prompt."""
    env_path = Path(temp_dir) / ".env"
    
    # Clear environment to avoid pollution
    env_backup = {}
    env_vars = ['DATABASE_PATH', 'YOUTUBE_MAX_RESULTS', 'WORKING_DIRECTORY']
    for var in env_vars:
        if var in os.environ:
            env_backup[var] = os.environ[var]
            del os.environ[var]
    
    try:
        # Create config in non-interactive mode
        config = Config(str(env_path), interactive=False)
        
        # Should use defaults without prompting
        assert config.database_path == "db.s3db"
        assert config.youtube_max_results == 50
    finally:
        # Restore environment variables
        for var, value in env_backup.items():
            os.environ[var] = value


def test_existing_env_values_preserved(temp_dir):
    """Test that existing .env values are preserved."""
    env_path = Path(temp_dir) / ".env"
    
    # Create .env with some values
    with open(env_path, 'w') as f:
        f.write("DATABASE_PATH=custom.db\n")
        f.write("YOUTUBE_MAX_RESULTS=100\n")
    
    # Create config
    config = Config(str(env_path), interactive=False)
    
    # Check that values are preserved
    assert config.database_path == "custom.db"
    assert config.youtube_max_results == 100
    
    # Check that working directory was added
    with open(env_path, 'r') as f:
        content = f.read()
        assert "WORKING_DIRECTORY=" in content
        assert "DATABASE_PATH=custom.db" in content
        assert "YOUTUBE_MAX_RESULTS=100" in content
