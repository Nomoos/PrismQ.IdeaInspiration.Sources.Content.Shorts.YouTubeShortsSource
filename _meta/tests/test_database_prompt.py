"""Test database creation confirmation prompt."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from mod.database import Database


def test_database_creation_prompt_yes():
    """Test that database is created when user confirms."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        # Simulate user confirming
        with patch('builtins.input', return_value='Y'):
            db = Database(db_path, interactive=True)
            assert Path(db_path).exists()
            db.close()


def test_database_creation_prompt_no():
    """Test that database creation is cancelled when user declines."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        # Simulate user declining
        with patch('builtins.input', return_value='N'):
            with pytest.raises(SystemExit):
                Database(db_path, interactive=True)
        
        # Database should not exist
        assert not Path(db_path).exists()


def test_database_no_prompt_when_exists():
    """Test that no prompt is shown when database already exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        # Create database first time (with confirmation)
        with patch('builtins.input', return_value='Y'):
            db1 = Database(db_path, interactive=True)
            db1.close()
        
        # Open again - should not prompt
        # If input is called, it will raise an error because we're not patching it
        db2 = Database(db_path, interactive=True)
        assert Path(db_path).exists()
        db2.close()


def test_database_no_prompt_when_not_interactive():
    """Test that no prompt is shown when interactive=False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        # Should not prompt when interactive=False
        # If input is called, it will raise an error because we're not patching it
        db = Database(db_path, interactive=False)
        assert Path(db_path).exists()
        db.close()
