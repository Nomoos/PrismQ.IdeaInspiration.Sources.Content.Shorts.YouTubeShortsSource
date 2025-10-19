"""Database context for CRUD operations on YouTube video data."""

from typing import Optional, List, Dict, Any
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from Model.base import Base
from Model.youtube_video import YouTubeVideo


class DBContext:
    """Database context for managing YouTube video data with CRUD operations.
    
    This class provides a clean interface for database operations using
    SQLAlchemy ORM with proper session management and error handling.
    Stores raw yt-dlp data without transformation.
    """
    
    def __init__(self, db_path: str = "ideas.db"):
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
    
    def create(self, video_id: str, ytdlp_data: Dict[str, Any]) -> Optional[YouTubeVideo]:
        """Create a new YouTube video record from yt-dlp data.
        
        Args:
            video_id: YouTube video ID (from yt-dlp's 'id' field)
            ytdlp_data: Complete yt-dlp data dictionary
            
        Returns:
            Created YouTubeVideo object or None on failure
        """
        session = self.SessionLocal()
        try:
            record = YouTubeVideo(video_id=video_id)
            record.set_raw_data(ytdlp_data)
            
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
            
        except IntegrityError:
            # Record with same video_id already exists
            session.rollback()
            return None
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def read(self, video_id: str) -> Optional[YouTubeVideo]:
        """Read a YouTube video record by video_id.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            YouTubeVideo object or None if not found
        """
        with self.get_session() as session:
            return session.query(YouTubeVideo).filter_by(video_id=video_id).first()
    
    def read_by_id(self, record_id: int) -> Optional[YouTubeVideo]:
        """Read a YouTube video record by database ID.
        
        Args:
            record_id: Database record ID
            
        Returns:
            YouTubeVideo object or None if not found
        """
        with self.get_session() as session:
            return session.query(YouTubeVideo).filter_by(id=record_id).first()
    
    def update(self, video_id: str, ytdlp_data: Dict[str, Any]) -> Optional[YouTubeVideo]:
        """Update an existing YouTube video record.
        
        Args:
            video_id: YouTube video ID
            ytdlp_data: Updated yt-dlp data dictionary
            
        Returns:
            Updated YouTubeVideo object or None if not found
        """
        with self.get_session() as session:
            record = session.query(YouTubeVideo).filter_by(video_id=video_id).first()
            
            if record:
                record.set_raw_data(ytdlp_data)
                session.commit()
                session.refresh(record)
                return record
            
            return None
    
    def upsert(self, video_id: str, ytdlp_data: Dict[str, Any]) -> YouTubeVideo:
        """Insert or update a YouTube video record.
        
        Args:
            video_id: YouTube video ID
            ytdlp_data: yt-dlp data dictionary
            
        Returns:
            YouTubeVideo object (created or updated)
        """
        existing = self.read(video_id)
        
        if existing:
            return self.update(video_id, ytdlp_data)
        else:
            return self.create(video_id, ytdlp_data)
    
    def delete(self, video_id: str) -> bool:
        """Delete a YouTube video record.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if deleted, False if not found
        """
        with self.get_session() as session:
            record = session.query(YouTubeVideo).filter_by(video_id=video_id).first()
            
            if record:
                session.delete(record)
                session.commit()
                return True
            
            return False
    
    def list_all(self, limit: Optional[int] = None,
                 order_by: str = 'created_at',
                 ascending: bool = False) -> List[YouTubeVideo]:
        """List all YouTube video records.
        
        Args:
            limit: Maximum number of results
            order_by: Column to order by ('id', 'video_id', 'created_at', 'updated_at')
            ascending: Sort in ascending order (default: descending)
            
        Returns:
            List of YouTubeVideo objects
        """
        with self.get_session() as session:
            query = session.query(YouTubeVideo)
            
            # Apply ordering
            order_column = getattr(YouTubeVideo, order_by, YouTubeVideo.created_at)
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
            return session.query(YouTubeVideo).count()
    
    def clear_all(self) -> int:
        """Clear all records from the database.
        
        Returns:
            Number of records deleted
        """
        with self.get_session() as session:
            count = session.query(YouTubeVideo).count()
            session.query(YouTubeVideo).delete()
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
