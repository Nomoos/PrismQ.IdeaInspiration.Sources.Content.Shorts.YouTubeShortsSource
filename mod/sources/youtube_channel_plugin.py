"""YouTube Channel source plugin for scraping idea inspirations from Shorts.

This plugin uses yt-dlp to scrape comprehensive metadata from YouTube channel Shorts,
including subtitles, video quality metrics, and detailed engagement analytics.
"""

import json
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from mod.sources import SourcePlugin


class YouTubeChannelPlugin(SourcePlugin):
    """Plugin for scraping ideas from YouTube channel Shorts using yt-dlp."""
    
    # YouTube Shorts constraints
    SHORTS_MAX_DURATION = 180  # 3 minutes max for Shorts
    SHORTS_FETCH_MULTIPLIER = 2  # Fetch extra to compensate for filtering
    
    def __init__(self, config):
        """Initialize YouTube channel plugin.
        
        Args:
            config: Configuration object
        """
        super().__init__(config)
        
        # Check if yt-dlp is available
        if not self._check_ytdlp():
            raise ValueError("yt-dlp is not installed. Install with: pip install yt-dlp")
    
    def get_source_name(self) -> str:
        """Get the name of this source.
        
        Returns:
            Source name
        """
        return "youtube_channel"
    
    def _check_ytdlp(self) -> bool:
        """Check if yt-dlp is installed.
        
        Returns:
            True if yt-dlp is available
        """
        try:
            result = subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def scrape(self, channel_url: Optional[str] = None, top_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Scrape ideas from YouTube channel Shorts.
        
        Args:
            channel_url: YouTube channel URL (optional, uses config if not provided)
            top_n: Number of shorts to scrape (optional, uses config if not provided)
        
        Returns:
            List of idea dictionaries
        """
        ideas = []
        
        # Use config values if not provided
        if channel_url is None:
            channel_url = getattr(self.config, 'youtube_channel_url', None)
            if not channel_url:
                print("Error: No channel URL provided and none configured")
                return ideas
        
        if top_n is None:
            top_n = getattr(self.config, 'youtube_channel_max_shorts', 10)
        
        # Extract channel URL format
        channel_url = self._normalize_channel_url(channel_url)
        
        # Get video IDs from channel shorts
        video_ids = self._get_channel_shorts(channel_url, top_n)
        
        if not video_ids:
            print(f"No shorts found for channel: {channel_url}")
            return ideas
        
        print(f"Found {len(video_ids)} shorts from channel")
        
        # Extract metadata for each video
        for i, video_id in enumerate(video_ids, 1):
            print(f"  [{i}/{len(video_ids)}] Extracting metadata for: {video_id}")
            metadata = self._extract_video_metadata(video_id)
            
            if metadata:
                # Convert to idea format
                idea = self._metadata_to_idea(metadata)
                if idea:
                    ideas.append(idea)
        
        return ideas
    
    def _normalize_channel_url(self, channel_input: str) -> str:
        """Normalize channel URL from various input formats.
        
        Args:
            channel_input: Channel URL, handle, or ID
        
        Returns:
            Normalized channel URL
        """
        # Already a full URL
        if channel_input.startswith('http'):
            return channel_input
        
        # Channel handle (starts with @)
        if channel_input.startswith('@'):
            return f"https://www.youtube.com/{channel_input}"
        
        # Channel ID (starts with UC)
        if channel_input.startswith('UC'):
            return f"https://www.youtube.com/channel/{channel_input}"
        
        # Assume it's a handle without @
        return f"https://www.youtube.com/@{channel_input}"
    
    def _get_channel_shorts(self, channel_url: str, top_n: int) -> List[str]:
        """Get list of video IDs from channel shorts.
        
        Args:
            channel_url: Channel URL
            top_n: Number of shorts to retrieve
        
        Returns:
            List of video IDs
        """
        shorts_url = channel_url.rstrip('/') + "/shorts"
        
        # Fetch more than needed to compensate for potential filtering
        fetch_count = top_n * self.SHORTS_FETCH_MULTIPLIER
        
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "id",
            "--playlist-end", str(fetch_count),
            "--playlist-reverse",  # Most recent first
            shorts_url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                video_ids = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                return video_ids[:top_n]
            else:
                print(f"Error fetching shorts: {result.stderr}")
                return []
        
        except subprocess.TimeoutExpired:
            print("Timeout while fetching shorts")
            return []
        except Exception as e:
            print(f"Error fetching shorts: {e}")
            return []
    
    def _extract_video_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Extract comprehensive metadata for a video using yt-dlp.
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Video metadata dictionary or None
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Use yt-dlp to get JSON metadata (no download)
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-info-json",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "srt",
            "-o", f"/tmp/yt_{video_id}",
            "--print", "{}",  # Suppress normal output
            video_url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Load the info JSON
            info_json_path = Path(f"/tmp/yt_{video_id}.info.json")
            
            if not info_json_path.exists():
                print(f"    Warning: Could not retrieve metadata for {video_id}")
                return None
            
            with open(info_json_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Extract subtitle text if available
            subtitle_text = None
            srt_files = list(Path("/tmp").glob(f"yt_{video_id}*.srt"))
            if srt_files:
                with open(srt_files[0], 'r', encoding='utf-8') as f:
                    subtitle_text = self._parse_srt_to_text(f.read())
            
            # Add subtitle text to metadata
            metadata['subtitle_text'] = subtitle_text
            
            # Clean up temporary files
            info_json_path.unlink(missing_ok=True)
            for srt_file in srt_files:
                srt_file.unlink(missing_ok=True)
            
            # Filter out non-shorts
            duration_seconds = metadata.get('duration', 0)
            if duration_seconds > self.SHORTS_MAX_DURATION:
                print(f"    Skipped: Video is too long ({duration_seconds}s > {self.SHORTS_MAX_DURATION}s)")
                return None
            
            # Check for vertical format (height > width)
            width = metadata.get('width', 0)
            height = metadata.get('height', 0)
            if height > 0 and width > 0 and height <= width:
                print(f"    Skipped: Video is not vertical format ({width}x{height})")
                return None
            
            return metadata
            
        except subprocess.TimeoutExpired:
            print(f"    Timeout extracting metadata for {video_id}")
            return None
        except Exception as e:
            print(f"    Error extracting metadata for {video_id}: {e}")
            return None
    
    def _parse_srt_to_text(self, srt_content: str) -> str:
        """Parse SRT subtitle file to plain text.
        
        Args:
            srt_content: Raw SRT file content
        
        Returns:
            Plain text of subtitles
        """
        lines = srt_content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines, numbers, and timestamp lines
            if not line or line.isdigit() or '-->' in line:
                continue
            text_lines.append(line)
        
        return ' '.join(text_lines)
    
    def _metadata_to_idea(self, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Convert yt-dlp metadata to idea format.
        
        Args:
            metadata: Video metadata from yt-dlp
        
        Returns:
            Idea dictionary
        """
        try:
            # Calculate engagement metrics
            view_count = metadata.get('view_count', 0)
            like_count = metadata.get('like_count', 0)
            comment_count = metadata.get('comment_count', 0)
            
            # Calculate engagement rate
            engagement_rate = 0.0
            if view_count > 0:
                engagement_rate = ((like_count + comment_count) / view_count) * 100
            
            # Calculate views per day
            views_per_day = 0.0
            upload_date_str = metadata.get('upload_date')
            if upload_date_str and view_count > 0:
                try:
                    upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                    days_since_upload = (datetime.now() - upload_date).days
                    if days_since_upload > 0:
                        views_per_day = view_count / days_since_upload
                except Exception:
                    pass
            
            # Extract video quality info
            resolution = f"{metadata.get('width', '?')}x{metadata.get('height', '?')}"
            fps = metadata.get('fps')
            aspect_ratio = None
            if metadata.get('width') and metadata.get('height'):
                width = metadata['width']
                height = metadata['height']
                aspect_ratio = f"{width}:{height}"
            
            # Build comprehensive metrics for UniversalMetrics
            metrics = {
                'id': metadata.get('id'),
                'snippet': {
                    'title': metadata.get('title', ''),
                    'description': metadata.get('description', ''),
                    'publishedAt': metadata.get('upload_date', ''),
                    'channelId': metadata.get('channel_id'),
                    'channelTitle': metadata.get('channel', metadata.get('uploader')),
                    'categoryId': str(metadata.get('categories', [''])[0]) if metadata.get('categories') else None,
                    'tags': metadata.get('tags', [])
                },
                'statistics': {
                    'viewCount': str(view_count),
                    'likeCount': str(like_count),
                    'commentCount': str(comment_count),
                    'favoriteCount': '0'
                },
                'contentDetails': {
                    'duration': self._format_duration_iso8601(metadata.get('duration', 0))
                },
                # Additional metrics not in standard YouTube API
                'enhanced_metrics': {
                    'engagement_rate': engagement_rate,
                    'views_per_day': views_per_day,
                    'resolution': resolution,
                    'fps': fps,
                    'aspect_ratio': aspect_ratio,
                    'subtitle_text': metadata.get('subtitle_text'),
                    'subtitles_available': bool(metadata.get('subtitle_text')),
                    'channel_follower_count': metadata.get('channel_follower_count')
                }
            }
            

            # Extract tags
            tags = self._extract_tags(metadata)
            
            return {
                'source_id': metadata.get('id'),
                'title': metadata.get('title', ''),
                'description': metadata.get('description', ''),
                'tags': tags,
                'metrics': metrics
            }
        
        except Exception as e:
            print(f"    Error converting metadata to idea: {e}")
            return None
    
    def _format_duration_iso8601(self, seconds: int) -> str:
        """Format duration in seconds to ISO 8601 format.
        
        Args:
            seconds: Duration in seconds
        
        Returns:
            ISO 8601 duration string (e.g., 'PT1M30S')
        """
        if seconds <= 0:
            return 'PT0S'
        
        minutes = seconds // 60
        secs = seconds % 60
        
        if minutes > 0:
            return f"PT{minutes}M{secs}S"
        else:
            return f"PT{secs}S"
    
    def _extract_tags(self, metadata: Dict[str, Any]) -> str:
        """Extract tags from video metadata.
        
        Args:
            metadata: Video metadata from yt-dlp
        
        Returns:
            Comma-separated tag string
        """
        tags = ['youtube_shorts', 'channel_short']
        
        # Add channel name
        channel = metadata.get('channel') or metadata.get('uploader')
        if channel:
            tags.append(channel)
        
        # Add categories
        categories = metadata.get('categories', [])
        if categories:
            tags.extend([f"category_{cat}" for cat in categories[:2]])
        
        # Add video tags
        video_tags = metadata.get('tags', [])
        if video_tags:
            tags.extend(video_tags[:5])  # Limit to first 5 tags
        
        return self.format_tags(tags)
