"""SQLAlchemy model for YouTube Shorts data."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
import json
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.orm import validates
from mod.Model.base import Base


def utc_now():
    """Get current UTC time in a timezone-aware manner."""
    return datetime.now(timezone.utc)


class YouTubeShortsSource(Base):
    """Model for storing YouTube Shorts idea inspirations.
    
    This model stores all scraped data from YouTube Shorts including
    metadata, metrics, and calculated scores.
    """
    
    __tablename__ = 'youtube_shorts_source'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Source information
    source = Column(String(100), nullable=False, index=True)
    source_id = Column(String(255), nullable=False, index=True)
    
    # Content fields
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    
    # Scoring
    score = Column(Float, nullable=True)
    score_dictionary = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_source_source_id', 'source', 'source_id', unique=True),
        Index('ix_score', 'score'),
        Index('ix_created_at', 'created_at'),
    )
    
    @validates('score_dictionary')
    def validate_score_dictionary(self, key, value):
        """Validate that score_dictionary is valid JSON."""
        if value is not None and isinstance(value, str):
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON for score_dictionary: {value}")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        return {
            'id': self.id,
            'source': self.source,
            'source_id': self.source_id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'score': self.score,
            'score_dictionary': self.score_dictionary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def get_score_dict(self) -> Optional[Dict[str, Any]]:
        """Get score dictionary as a Python dict.
        
        Returns:
            Parsed score dictionary or None
        """
        if self.score_dictionary:
            try:
                return json.loads(self.score_dictionary)
            except json.JSONDecodeError:
                return None
        return None
    
    def set_score_dict(self, score_dict: Dict[str, Any]) -> None:
        """Set score dictionary from a Python dict.
        
        Args:
            score_dict: Dictionary to store
        """
        if score_dict is not None:
            self.score_dictionary = json.dumps(score_dict)
        else:
            self.score_dictionary = None
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<YouTubeShortsSource(id={self.id}, source='{self.source}', source_id='{self.source_id}', title='{self.title[:50]}...')>"
