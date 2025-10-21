"""Database models and schema for PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource.

This module provides backward compatibility with the original SQLite-based Database class
while internally using the new SQLAlchemy ORM model layer.
"""

import sqlite3
from typing import Optional, Dict, Any
import json
from pathlib import Path
from mod.Model import DBContext


class Database:
    """Manages SQLite database operations for idea collection.
    
    This class now wraps the new DBContext for backward compatibility
    with existing code while using SQLAlchemy ORM internally.
    """

    def __init__(self, db_path: str):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        
        # Use new DBContext internally
        self.db_context = DBContext(db_path)
        
        # For backward compatibility, also maintain a raw SQLite connection
        self._init_db()

    def _init_db(self):
        """Initialize database schema if it doesn't exist."""
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create raw SQLite connection for backward compatibility
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        # Also create the old 'ideas' table for backward compatibility with tests
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
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
            )
        """)
        self.connection.commit()

    def insert_idea(self, source: str, source_id: str, title: str, 
                   description: Optional[str] = None, tags: Optional[str] = None,
                   score: Optional[float] = None, 
                   score_dictionary: Optional[Dict[str, Any]] = None) -> bool:
        """Insert or update an idea in the database.
        
        Args:
            source: Source platform (e.g., 'youtube', 'reddit')
            source_id: Unique identifier from the source
            title: Idea title
            description: Idea description
            tags: Comma-separated tags
            score: Calculated score
            score_dictionary: Dictionary of score components
            
        Returns:
            True if inserted/updated, False otherwise
        """
        try:
            # Use new model's upsert method
            result = self.db_context.upsert(
                source=source,
                source_id=source_id,
                title=title,
                description=description,
                tags=tags,
                score=score,
                score_dictionary=score_dictionary
            )
            return result is not None
        except Exception as e:
            print(f"Database error: {e}")
            return False

    def get_idea(self, source: str, source_id: str) -> Optional[Dict[str, Any]]:
        """Get an idea by source and source_id.
        
        Args:
            source: Source platform
            source_id: Source-specific ID
            
        Returns:
            Dictionary with idea data or None if not found
        """
        record = self.db_context.read(source, source_id)
        if record:
            return record.to_dict()
        return None

    def get_all_ideas(self, limit: Optional[int] = None, 
                     order_by: str = 'score DESC') -> list:
        """Get all ideas from the database.
        
        Args:
            limit: Maximum number of results
            order_by: SQL ORDER BY clause (validated for safety)
            
        Returns:
            List of idea dictionaries
        """
        # Validate limit first
        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise ValueError(f"Invalid limit value: {limit}")
        
        # Parse order_by to determine column and direction
        parts = order_by.strip().split()
        column = 'score'
        ascending = False
        
        # Validate column and direction
        allowed_columns = {'id', 'source', 'source_id', 'title', 'score', 'created_at', 'updated_at'}
        
        if len(parts) >= 1:
            column = parts[0].lower()
            if column not in allowed_columns:
                raise ValueError(f"Invalid order_by column: {column}")
        if len(parts) >= 2:
            direction = parts[1].upper()
            if direction not in {'ASC', 'DESC'}:
                raise ValueError(f"Invalid order direction: {direction}")
            ascending = direction == 'ASC'
        
        # Map old column names to model attributes
        column_map = {
            'id': 'id',
            'source': 'source',
            'source_id': 'source_id',
            'title': 'title',
            'score': 'score',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }
        
        # Use mapped column name or default to score
        order_column = column_map.get(column, 'score')
        
        try:
            records = self.db_context.list_all(
                limit=limit,
                order_by=order_column,
                ascending=ascending
            )
            return [record.to_dict() for record in records]
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
        if hasattr(self, 'db_context'):
            self.db_context.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

