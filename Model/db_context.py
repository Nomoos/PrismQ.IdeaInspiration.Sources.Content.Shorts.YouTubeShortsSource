"""Database context for CRUD operations on YouTube Shorts data."""

from typing import Optional, List, Dict, Any
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from mod.Model.base import Base
from mod.Model.youtube_shorts_source import YouTubeShortsSource


class DBContext:
    """Database context for managing YouTube Shorts data with CRUD operations.
    
    This class provides a clean interface for database operations using
    SQLAlchemy ORM with proper session management and error handling.
    """
    
    def __init__(self, db_path: str = "db.s3db"):
        """Initialize database context.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create engine and session factory
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        
        # Initialize database schema
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema if it doesn't exist."""
        Base.metadata.create_all(self.engine)
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a database session with automatic cleanup.
        
        Yields:
            SQLAlchemy session
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create(self, source: str, source_id: str, title: str,
               description: Optional[str] = None, tags: Optional[str] = None,
               score: Optional[float] = None,
               score_dictionary: Optional[Dict[str, Any]] = None) -> Optional[YouTubeShortsSource]:
        """Create a new YouTube Shorts record.
        
        Args:
            source: Source platform (e.g., 'youtube')
            source_id: Unique identifier from the source
            title: Video title
            description: Video description
            tags: Comma-separated tags
            score: Calculated score
            score_dictionary: Dictionary of score components
            
        Returns:
            Created YouTubeShortsSource object or None on failure
        """
        session = self.SessionLocal()
        try:
            record = YouTubeShortsSource(
                source=source,
                source_id=source_id,
                title=title,
                description=description,
                tags=tags,
                score=score
            )
            
            if score_dictionary:
                record.set_score_dict(score_dictionary)
            
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
            
        except IntegrityError:
            # Record with same source and source_id already exists
            session.rollback()
            return None
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def read(self, source: str, source_id: str) -> Optional[YouTubeShortsSource]:
        """Read a YouTube Shorts record by source and source_id.
        
        Args:
            source: Source platform
            source_id: Source-specific ID
            
        Returns:
            YouTubeShortsSource object or None if not found
        """
        with self.get_session() as session:
            return session.query(YouTubeShortsSource).filter_by(
                source=source,
                source_id=source_id
            ).first()
    
    def read_by_id(self, record_id: int) -> Optional[YouTubeShortsSource]:
        """Read a YouTube Shorts record by ID.
        
        Args:
            record_id: Database record ID
            
        Returns:
            YouTubeShortsSource object or None if not found
        """
        with self.get_session() as session:
            return session.query(YouTubeShortsSource).filter_by(id=record_id).first()
    
    def update(self, source: str, source_id: str,
               title: Optional[str] = None,
               description: Optional[str] = None,
               tags: Optional[str] = None,
               score: Optional[float] = None,
               score_dictionary: Optional[Dict[str, Any]] = None,
               processed: Optional[bool] = None) -> Optional[YouTubeShortsSource]:
        """Update an existing YouTube Shorts record.
        
        Args:
            source: Source platform
            source_id: Source-specific ID
            title: New title (optional)
            description: New description (optional)
            tags: New tags (optional)
            score: New score (optional)
            score_dictionary: New score dictionary (optional)
            processed: New processed status (optional)
            
        Returns:
            Updated YouTubeShortsSource object or None if not found
        """
        with self.get_session() as session:
            record = session.query(YouTubeShortsSource).filter_by(
                source=source,
                source_id=source_id
            ).first()
            
            if record:
                if title is not None:
                    record.title = title
                if description is not None:
                    record.description = description
                if tags is not None:
                    record.tags = tags
                if score is not None:
                    record.score = score
                if score_dictionary is not None:
                    record.set_score_dict(score_dictionary)
                if processed is not None:
                    record.processed = processed
                
                session.commit()
                session.refresh(record)
                return record
            
            return None
    
    def upsert(self, source: str, source_id: str, title: str,
               description: Optional[str] = None, tags: Optional[str] = None,
               score: Optional[float] = None,
               score_dictionary: Optional[Dict[str, Any]] = None) -> YouTubeShortsSource:
        """Insert or update a YouTube Shorts record.
        
        Args:
            source: Source platform
            source_id: Source-specific ID
            title: Video title
            description: Video description
            tags: Comma-separated tags
            score: Calculated score
            score_dictionary: Dictionary of score components
            
        Returns:
            YouTubeShortsSource object (created or updated)
        """
        existing = self.read(source, source_id)
        
        if existing:
            return self.update(
                source=source,
                source_id=source_id,
                title=title,
                description=description,
                tags=tags,
                score=score,
                score_dictionary=score_dictionary
            )
        else:
            return self.create(
                source=source,
                source_id=source_id,
                title=title,
                description=description,
                tags=tags,
                score=score,
                score_dictionary=score_dictionary
            )
    
    def delete(self, source: str, source_id: str) -> bool:
        """Delete a YouTube Shorts record.
        
        Args:
            source: Source platform
            source_id: Source-specific ID
            
        Returns:
            True if deleted, False if not found
        """
        with self.get_session() as session:
            record = session.query(YouTubeShortsSource).filter_by(
                source=source,
                source_id=source_id
            ).first()
            
            if record:
                session.delete(record)
                session.commit()
                return True
            
            return False
    
    def list_all(self, limit: Optional[int] = None,
                 order_by: str = 'score',
                 ascending: bool = False) -> List[YouTubeShortsSource]:
        """List all YouTube Shorts records.
        
        Args:
            limit: Maximum number of results
            order_by: Column to order by ('score', 'created_at', 'updated_at')
            ascending: Sort in ascending order (default: descending)
            
        Returns:
            List of YouTubeShortsSource objects
        """
        with self.get_session() as session:
            query = session.query(YouTubeShortsSource)
            
            # Apply ordering
            order_column = getattr(YouTubeShortsSource, order_by, YouTubeShortsSource.score)
            if ascending:
                query = query.order_by(asc(order_column))
            else:
                query = query.order_by(desc(order_column))
            
            # Apply limit
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def count(self) -> int:
        """Get total count of records.
        
        Returns:
            Total number of records
        """
        with self.get_session() as session:
            return session.query(YouTubeShortsSource).count()
    
    def count_by_source(self, source: str) -> int:
        """Get count of records by source.
        
        Args:
            source: Source platform
            
        Returns:
            Number of records from the source
        """
        with self.get_session() as session:
            return session.query(YouTubeShortsSource).filter_by(source=source).count()
    
    def clear_all(self) -> int:
        """Clear all records from the database.
        
        Returns:
            Number of records deleted
        """
        with self.get_session() as session:
            count = session.query(YouTubeShortsSource).count()
            session.query(YouTubeShortsSource).delete()
            session.commit()
            return count
    
    def close(self):
        """Close database connection."""
        if hasattr(self, 'engine'):
            self.engine.dispose()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
