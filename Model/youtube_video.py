"""SQLAlchemy model for YouTube video data from yt-dlp."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
import json
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.orm import validates
from Model.base import Base


def utc_now():
    """Get current UTC time in a timezone-aware manner."""
    return datetime.now(timezone.utc)


class YouTubeVideo(Base):
    """Model for storing YouTube video data from yt-dlp.
    
    This model stores the raw yt-dlp data without transformation,
    preserving all metadata extracted by yt-dlp.
    """
    
    __tablename__ = 'youtube_video'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Video ID (from yt-dlp's 'id' field)
    video_id = Column(String(255), nullable=False, unique=True, index=True)
    
    # Raw yt-dlp data stored as JSON
    # This preserves all fields extracted by yt-dlp without transformation
    raw_data = Column(Text, nullable=False)
    
    # Timestamps for record management
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_video_id', 'video_id', unique=True),
        Index('ix_created_at', 'created_at'),
    )
    
    @validates('raw_data')
    def validate_raw_data(self, key, value):
        """Validate that raw_data is valid JSON."""
        if value is not None and isinstance(value, str):
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON for raw_data: {value}")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        return {
            'id': self.id,
            'video_id': self.video_id,
            'raw_data': self.raw_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def get_raw_data(self) -> Optional[Dict[str, Any]]:
        """Get raw yt-dlp data as a Python dict.
        
        Returns:
            Parsed yt-dlp data or None
        """
        if self.raw_data:
            try:
                return json.loads(self.raw_data)
            except json.JSONDecodeError:
                return None
        return None
    
    def set_raw_data(self, data: Dict[str, Any]) -> None:
        """Set raw yt-dlp data from a Python dict.
        
        Args:
            data: yt-dlp data dictionary to store
        """
        if data is not None:
            self.raw_data = json.dumps(data)
        else:
            self.raw_data = None
    
    def get_field(self, field_name: str, default=None):
        """Get a specific field from raw yt-dlp data.
        
        Args:
            field_name: Name of the field to retrieve
            default: Default value if field doesn't exist
            
        Returns:
            Field value or default
        """
        data = self.get_raw_data()
        if data:
            return data.get(field_name, default)
        return default
    
    def __repr__(self) -> str:
        """String representation of the model."""
        title = self.get_field('title', 'Unknown')
        return f"<YouTubeVideo(id={self.id}, video_id='{self.video_id}', title='{title[:50]}...')>"
