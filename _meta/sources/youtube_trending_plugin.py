"""YouTube Trending and Keyword source plugin for scraping idea inspirations from Shorts.

This plugin uses yt-dlp to scrape Shorts from YouTube trending and keyword searches,
providing comprehensive metadata extraction without API quota limits.
"""

import json
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from mod.sources import SourcePlugin


class YouTubeTrendingPlugin(SourcePlugin):
    """Plugin for scraping ideas from YouTube Trending and keyword searches using yt-dlp."""
    
    # YouTube Shorts constraints
    SHORTS_MAX_DURATION = 180  # 3 minutes max for Shorts
    SHORTS_FETCH_MULTIPLIER = 3  # Fetch extra to compensate for filtering
    
    def __init__(self, config):
        """Initialize YouTube trending plugin.
        
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
        return "youtube_trending"
    
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
    
    def scrape_trending(self, top_n: Optional[int] = None, category: str = "all") -> List[Dict[str, Any]]:
        """Scrape Shorts from YouTube trending.
        
        Args:
            top_n: Number of shorts to scrape (optional, uses config if not provided)
            category: Trending category (default: "all")
        
        Returns:
            List of idea dictionaries
        """
        ideas = []
        
        if top_n is None:
            top_n = getattr(self.config, 'youtube_trending_max_shorts', 10)
        
        print(f"Scraping trending Shorts...")
        
        # YouTube trending URL
        trending_url = "https://www.youtube.com/feed/trending"
        
        # Get video IDs from trending
        video_ids = self._get_trending_videos(trending_url, top_n)
        
        if not video_ids:
            print(f"No trending videos found")
            return ideas
        
        print(f"Found {len(video_ids)} trending videos")
        
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
    
    def scrape_by_keyword(self, keyword: str, top_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Scrape Shorts by keyword search.
        
        Args:
            keyword: Search keyword
            top_n: Number of shorts to scrape (optional, uses config if not provided)
        
        Returns:
            List of idea dictionaries
        """
        ideas = []
        
        if top_n is None:
            top_n = getattr(self.config, 'youtube_keyword_max_shorts', 10)
        
        print(f"Scraping Shorts with keyword: '{keyword}'...")
        
        # Get video IDs from keyword search
        video_ids = self._search_by_keyword(keyword, top_n)
        
        if not video_ids:
            print(f"No videos found for keyword: '{keyword}'")
            return ideas
        
        print(f"Found {len(video_ids)} videos for keyword: '{keyword}'")
        
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
    
    def scrape(self, keyword: Optional[str] = None, trending: bool = False, top_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Main scrape method that delegates to trending or keyword scraping.
        
        Args:
            keyword: Search keyword (if provided, does keyword search)
            trending: If True, scrapes from trending (default: False)
            top_n: Number of shorts to scrape
        
        Returns:
            List of idea dictionaries
        """
        if trending:
            return self.scrape_trending(top_n=top_n)
        elif keyword:
            return self.scrape_by_keyword(keyword, top_n=top_n)
        else:
            # Default to trending if no keyword specified
            return self.scrape_trending(top_n=top_n)
    
    def _get_trending_videos(self, trending_url: str, top_n: int) -> List[str]:
        """Get list of video IDs from trending page.
        
        Args:
            trending_url: YouTube trending URL
            top_n: Number of videos to retrieve
        
        Returns:
            List of video IDs
        """
        # Fetch more than needed to compensate for non-Shorts
        fetch_count = top_n * self.SHORTS_FETCH_MULTIPLIER
        
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "id",
            "--playlist-end", str(fetch_count),
            trending_url
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
                return video_ids[:fetch_count]
            else:
                print(f"Error fetching trending videos: {result.stderr}")
                return []
        
        except subprocess.TimeoutExpired:
            print("Timeout while fetching trending videos")
            return []
        except Exception as e:
            print(f"Error fetching trending videos: {e}")
            return []
    
    def _search_by_keyword(self, keyword: str, top_n: int) -> List[str]:
        """Search for videos by keyword.
        
        Args:
            keyword: Search keyword
            top_n: Number of videos to retrieve
        
        Returns:
            List of video IDs
        """
        # Fetch more than needed to compensate for non-Shorts
        fetch_count = top_n * self.SHORTS_FETCH_MULTIPLIER
        
        # Construct search URL - use ytsearch: prefix for keyword search
        search_query = f"ytsearch{fetch_count}:{keyword} shorts"
        
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "id",
            search_query
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
                return video_ids
            else:
                print(f"Error searching for keyword: {result.stderr}")
                return []
        
        except subprocess.TimeoutExpired:
            print("Timeout while searching for keyword")
            return []
        except Exception as e:
            print(f"Error searching for keyword: {e}")
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
            
            # Check for vertical format (height > width) - relaxed for trending/keyword
            width = metadata.get('width', 0)
            height = metadata.get('height', 0)
            # Note: We're more lenient here since trending may include various formats
            
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
        tags = ['youtube_shorts', 'trending']
        
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
