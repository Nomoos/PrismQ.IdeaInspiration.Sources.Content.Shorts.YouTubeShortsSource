"""Processor for transforming YouTube Shorts data to IdeaInspiration model.

This module provides functionality to transform YouTubeShortsSource database
records into the standardized IdeaInspiration format as defined in
PrismQ.IdeaInspiration.Model.
"""

import json
from typing import Optional, Dict, Any, List
from datetime import datetime


class ContentType:
    """Type of content source (matching PrismQ.IdeaInspiration.Model)."""
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    UNKNOWN = "unknown"


class IdeaInspiration:
    """Standardized IdeaInspiration model (matching PrismQ.IdeaInspiration.Model).
    
    This is a lightweight version for transformation purposes. The full model
    is defined in PrismQ.IdeaInspiration.Model repository.
    """
    
    def __init__(
        self,
        title: str,
        description: str = "",
        content: str = "",
        keywords: Optional[List[str]] = None,
        source_type: str = ContentType.UNKNOWN,
        metadata: Optional[Dict[str, str]] = None,
        source_id: Optional[str] = None,
        source_url: Optional[str] = None,
        source_created_by: Optional[str] = None,
        source_created_at: Optional[str] = None,
        score: Optional[int] = None,
        category: Optional[str] = None,
        subcategory_relevance: Optional[Dict[str, int]] = None,
        contextual_category_scores: Optional[Dict[str, int]] = None,
    ):
        """Initialize IdeaInspiration.
        
        Args:
            title: Content title
            description: Brief description
            content: Main text content (subtitles/transcription for video)
            keywords: List of keywords
            source_type: Type of content (text/video/audio)
            metadata: Additional metadata (string key-value pairs)
            source_id: Source platform identifier
            source_url: URL to original content
            source_created_by: Creator/author
            source_created_at: Creation timestamp (ISO 8601)
            score: Numerical score
            category: Primary category
            subcategory_relevance: Relevance scores for subcategories
            contextual_category_scores: Contextual scores by language/region/age/gender
        """
        self.title = title
        self.description = description
        self.content = content
        self.keywords = keywords or []
        self.source_type = source_type
        self.metadata = metadata or {}
        self.source_id = source_id
        self.source_url = source_url
        self.source_created_by = source_created_by
        self.source_created_at = source_created_at
        self.score = score
        self.category = category
        self.subcategory_relevance = subcategory_relevance or {}
        self.contextual_category_scores = contextual_category_scores or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation.
        
        Returns:
            Dictionary containing all fields
        """
        return {
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'keywords': self.keywords,
            'source_type': self.source_type,
            'metadata': self.metadata,
            'source_id': self.source_id,
            'source_url': self.source_url,
            'source_created_by': self.source_created_by,
            'source_created_at': self.source_created_at,
            'score': self.score,
            'category': self.category,
            'subcategory_relevance': self.subcategory_relevance,
            'contextual_category_scores': self.contextual_category_scores,
        }


class IdeaProcessor:
    """Processor for transforming YouTube Shorts data to IdeaInspiration format.
    
    This class handles the transformation of YouTubeShortsSource database records
    into the standardized IdeaInspiration model format as specified in
    PrismQ.IdeaInspiration.Model.
    """
    
    @staticmethod
    def process(youtube_shorts_record: Any) -> IdeaInspiration:
        """Transform YouTubeShortsSource record to IdeaInspiration.
        
        Args:
            youtube_shorts_record: YouTubeShortsSource database record (dict or object)
            
        Returns:
            IdeaInspiration instance
            
        Raises:
            ValueError: If required fields are missing
        """
        if not youtube_shorts_record:
            raise ValueError("Record cannot be None")
        
        # Support both dict and object access patterns
        def get_field(record, field):
            if isinstance(record, dict):
                return record.get(field)
            else:
                return getattr(record, field, None)
        
        title = get_field(youtube_shorts_record, 'title')
        source_id = get_field(youtube_shorts_record, 'source_id')
        
        if not title:
            raise ValueError("Record must have a title")
        
        if not source_id:
            raise ValueError("Record must have a source_id")
        
        # Parse score_dictionary to extract metadata
        score_dictionary = get_field(youtube_shorts_record, 'score_dictionary')
        if isinstance(youtube_shorts_record, dict):
            # For dict, parse JSON if it's a string
            if isinstance(score_dictionary, str):
                import json
                try:
                    score_dict = json.loads(score_dictionary) if score_dictionary else {}
                except json.JSONDecodeError:
                    score_dict = {}
            else:
                score_dict = score_dictionary or {}
        else:
            # For ORM objects, call get_score_dict method if available
            if hasattr(youtube_shorts_record, 'get_score_dict'):
                score_dict = youtube_shorts_record.get_score_dict() or {}
            else:
                score_dict = {}
        
        # Extract subtitle/transcription text from enhanced_metrics
        content = ""
        enhanced_metrics = score_dict.get('enhanced_metrics', {})
        if enhanced_metrics and enhanced_metrics.get('subtitle_text'):
            content = enhanced_metrics['subtitle_text']
        
        # Extract keywords from tags (comma-separated string)
        keywords = []
        tags = get_field(youtube_shorts_record, 'tags')
        if tags:
            keywords = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Build metadata dictionary (string key-value pairs for SQLite compatibility)
        metadata = IdeaProcessor._build_metadata(youtube_shorts_record, score_dict)
        
        # Extract source information
        source_url = IdeaProcessor._build_source_url(source_id)
        source_created_by = IdeaProcessor._extract_channel_name(score_dict)
        source_created_at = IdeaProcessor._extract_upload_date(score_dict)
        
        # Calculate score (use existing score or convert to int)
        record_score = get_field(youtube_shorts_record, 'score')
        score = None
        if record_score is not None:
            # Round to nearest integer for IdeaInspiration model
            score = int(round(record_score))
        
        description = get_field(youtube_shorts_record, 'description')
        
        return IdeaInspiration(
            title=title,
            description=description or "",
            content=content,
            keywords=keywords,
            source_type=ContentType.VIDEO,  # YouTube Shorts are video content
            metadata=metadata,
            source_id=source_id,
            source_url=source_url,
            source_created_by=source_created_by,
            source_created_at=source_created_at,
            score=score,
        )
    
    @staticmethod
    def _build_metadata(record: Any, score_dict: Dict[str, Any]) -> Dict[str, str]:
        """Build metadata dictionary from record and score dictionary.
        
        Args:
            record: YouTubeShortsSource record (dict or object)
            score_dict: Parsed score dictionary
            
        Returns:
            Metadata dictionary (string key-value pairs)
        """
        metadata = {}
        
        # Extract statistics
        statistics = score_dict.get('statistics', {})
        if statistics:
            metadata['views'] = str(statistics.get('viewCount', '0'))
            metadata['likes'] = str(statistics.get('likeCount', '0'))
            metadata['comments'] = str(statistics.get('commentCount', '0'))
        
        # Extract content details
        content_details = score_dict.get('contentDetails', {})
        if content_details:
            metadata['duration'] = str(content_details.get('duration', ''))
        
        # Extract enhanced metrics
        enhanced_metrics = score_dict.get('enhanced_metrics', {})
        if enhanced_metrics:
            if enhanced_metrics.get('engagement_rate') is not None:
                metadata['engagement_rate'] = str(enhanced_metrics['engagement_rate'])
            if enhanced_metrics.get('views_per_day') is not None:
                metadata['views_per_day'] = str(enhanced_metrics['views_per_day'])
            if enhanced_metrics.get('resolution'):
                metadata['resolution'] = str(enhanced_metrics['resolution'])
            if enhanced_metrics.get('fps') is not None:
                metadata['fps'] = str(enhanced_metrics['fps'])
            if enhanced_metrics.get('aspect_ratio'):
                metadata['aspect_ratio'] = str(enhanced_metrics['aspect_ratio'])
            if enhanced_metrics.get('subtitles_available') is not None:
                metadata['subtitles_available'] = str(enhanced_metrics['subtitles_available'])
            if enhanced_metrics.get('channel_follower_count') is not None:
                metadata['channel_follower_count'] = str(enhanced_metrics['channel_follower_count'])
        
        # Extract snippet data
        snippet = score_dict.get('snippet', {})
        if snippet:
            if snippet.get('channelId'):
                metadata['channel_id'] = str(snippet['channelId'])
            if snippet.get('channelTitle'):
                metadata['channel_title'] = str(snippet['channelTitle'])
            if snippet.get('publishedAt'):
                metadata['published_at'] = str(snippet['publishedAt'])
            if snippet.get('categoryId'):
                metadata['category_id'] = str(snippet['categoryId'])
        
        # Add platform identifier
        metadata['platform'] = 'youtube_shorts'
        metadata['source_type'] = 'video'
        
        return metadata
    
    @staticmethod
    def _build_source_url(source_id: str) -> str:
        """Build YouTube Shorts URL from video ID.
        
        Args:
            source_id: YouTube video ID
            
        Returns:
            Full YouTube Shorts URL
        """
        return f"https://www.youtube.com/shorts/{source_id}"
    
    @staticmethod
    def _extract_channel_name(score_dict: Dict[str, Any]) -> Optional[str]:
        """Extract channel name from score dictionary.
        
        Args:
            score_dict: Parsed score dictionary
            
        Returns:
            Channel name or None
        """
        snippet = score_dict.get('snippet', {})
        return snippet.get('channelTitle')
    
    @staticmethod
    def _extract_upload_date(score_dict: Dict[str, Any]) -> Optional[str]:
        """Extract and format upload date from score dictionary.
        
        Args:
            score_dict: Parsed score dictionary
            
        Returns:
            ISO 8601 formatted date string or None
        """
        snippet = score_dict.get('snippet', {})
        published_at = snippet.get('publishedAt')
        
        if not published_at:
            return None
        
        # Try to parse and convert to ISO 8601 format
        # Handle both YYYYMMDD and ISO 8601 formats
        try:
            if len(published_at) == 8 and published_at.isdigit():
                # YYYYMMDD format
                dt = datetime.strptime(published_at, '%Y%m%d')
                return dt.isoformat()
            else:
                # Assume it's already in ISO 8601 or similar format
                return published_at
        except ValueError:
            # If parsing fails, return as-is
            return published_at
    
    @staticmethod
    def process_batch(records: List[Any]) -> List[IdeaInspiration]:
        """Process multiple YouTube Shorts records in batch.
        
        Args:
            records: List of YouTubeShortsSource records
            
        Returns:
            List of IdeaInspiration instances
        """
        results = []
        for record in records:
            try:
                idea = IdeaProcessor.process(record)
                results.append(idea)
            except ValueError as e:
                # Log error but continue processing
                print(f"Warning: Failed to process record {record.id}: {e}")
                continue
        return results
