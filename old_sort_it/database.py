"""Database wrapper for backward compatibility.

This module provides backward compatibility with the original Database class
by wrapping the new db_utils module that uses DATABASE_URL.
"""

import sys
from typing import Optional, List, Dict, Any
from pathlib import Path
import db_utils


class Database:
    """Manages database operations for idea collection.
    
    This class wraps db_utils for backward compatibility with existing code.
    """

    def __init__(self, db_path: str, interactive: bool = True):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file (or use database_url directly)
            interactive: Whether to prompt for confirmation before creating database
        """
        self.db_path = db_path
        self._interactive = interactive
        
        # Construct database_url from db_path
        if db_path.startswith("sqlite://"):
            self.database_url = db_path
        else:
            self.database_url = f"sqlite:///{db_path}"
        
        # Check if database already exists
        db_exists = Path(db_path).exists() if not db_path.startswith("sqlite://") else True
        
        # If database doesn't exist and we're in interactive mode, ask for confirmation
        if not db_exists and self._interactive:
            if not self._confirm_database_creation():
                print("Database creation cancelled.")
                sys.exit(0)
        
        # Initialize database schema
        self._init_db()
    
    def _confirm_database_creation(self) -> bool:
        """Prompt user for confirmation before creating database.
        
        Returns:
            True if user confirms, False otherwise
        """
        try:
            response = input(f"Database '{self.db_path}' does not exist. Create it? (y/n): ").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            # In non-interactive environments, return True
            return True
    
    def _init_db(self):
        """Initialize database schema."""
        db_utils.init_database(self.database_url)
    
    def insert_idea(self, source: str, source_id: str, title: str,
                   description: Optional[str] = None, tags: Optional[str] = None,
                   score: Optional[float] = None, score_dictionary: Optional[str] = None) -> bool:
        """Insert or update an idea in the database.
        
        Args:
            source: Source platform
            source_id: Unique identifier from source
            title: Video title
            description: Video description
            tags: Comma-separated tags
            score: Calculated score
            score_dictionary: JSON string or dict of score components
            
        Returns:
            True if inserted, False if updated (duplicate)
        """
        # Convert dict to JSON string if needed
        if isinstance(score_dictionary, dict):
            import json
            score_dictionary = json.dumps(score_dictionary)
        
        return db_utils.insert_idea(
            self.database_url, source, source_id, title,
            description, tags, score, score_dictionary
        )
    
    def get_idea(self, source: str, source_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific idea by source and source_id.
        
        Args:
            source: Source platform
            source_id: Unique identifier from source
            
        Returns:
            Idea dictionary or None if not found
        """
        from sqlalchemy import text
        with db_utils.get_connection(self.database_url) as conn:
            result = conn.execute(
                text("SELECT * FROM YouTubeShortsSource WHERE source = :source AND source_id = :source_id"),
                {"source": source, "source_id": source_id}
            )
            row = result.fetchone()
            if row:
                return dict(zip(result.keys(), row))
            return None
    
    def get_all_ideas(self, limit: int = 20, order_by: str = "score") -> List[Dict[str, Any]]:
        """Get all ideas from database.
        
        Args:
            limit: Maximum number of records to return
            order_by: Column to order by
            
        Returns:
            List of idea dictionaries
        """
        return db_utils.get_all_ideas(self.database_url, limit, order_by)
    
    def count_ideas(self) -> int:
        """Count total ideas in database.
        
        Returns:
            Total count
        """
        return db_utils.count_ideas(self.database_url)
    
    def count_by_source(self, source: str) -> int:
        """Count ideas by source.
        
        Args:
            source: Source platform
            
        Returns:
            Count for source
        """
        return db_utils.count_by_source(self.database_url, source)
    
    def close(self):
        """Close database connection (no-op for backward compatibility)."""
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
