"""Database models and schema for PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource."""

import sqlite3
from typing import Optional, Dict, Any
import json
from pathlib import Path


class Database:
    """Manages SQLite database operations for idea collection."""

    def __init__(self, db_path: str):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self._init_db()

    def _init_db(self):
        """Initialize database schema if it doesn't exist."""
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        
        # Create ideas table with all required fields
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
        
        # Create index for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source_source_id 
            ON ideas(source, source_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_score 
            ON ideas(score DESC)
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
        cursor = self.connection.cursor()
        
        # Convert score_dictionary to JSON string
        score_dict_str = json.dumps(score_dictionary) if score_dictionary else None
        
        try:
            cursor.execute("""
                INSERT INTO ideas (source, source_id, title, description, tags, score, score_dictionary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source, source_id) DO UPDATE SET
                    title = excluded.title,
                    description = excluded.description,
                    tags = excluded.tags,
                    score = excluded.score,
                    score_dictionary = excluded.score_dictionary,
                    updated_at = CURRENT_TIMESTAMP
            """, (source, source_id, title, description, tags, score, score_dict_str))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
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
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM ideas WHERE source = ? AND source_id = ?
        """, (source, source_id))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
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
        # Validate order_by to prevent SQL injection
        # Only allow safe column names and ASC/DESC
        allowed_columns = {'id', 'source', 'source_id', 'title', 'score', 'created_at', 'updated_at'}
        allowed_directions = {'ASC', 'DESC', ''}
        
        # Check for SQL injection attempts (semicolons, comments, etc.)
        if ';' in order_by or '--' in order_by or '/*' in order_by or 'DROP' in order_by.upper():
            raise ValueError(f"Invalid order_by clause: potentially malicious input detected")
        
        # Parse order_by clause
        order_parts = order_by.strip().split()
        if len(order_parts) == 0:
            order_by = 'score DESC'
        elif len(order_parts) == 1:
            column = order_parts[0].lower()
            if column not in allowed_columns:
                raise ValueError(f"Invalid order_by column: {column}")
            order_by = f"{column} DESC"
        elif len(order_parts) == 2:
            column = order_parts[0].lower()
            direction = order_parts[1].upper()
            if column not in allowed_columns:
                raise ValueError(f"Invalid order_by column: {column}")
            if direction not in allowed_directions:
                raise ValueError(f"Invalid order direction: {direction}")
            order_by = f"{column} {direction}"
        else:
            # For complex cases, just use default for security
            raise ValueError(f"Invalid order_by clause: too complex")
        
        cursor = self.connection.cursor()
        query = f"SELECT * FROM ideas ORDER BY {order_by}"
        
        if limit:
            # Validate limit is an integer
            if not isinstance(limit, int) or limit < 0:
                raise ValueError(f"Invalid limit value: {limit}")
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
