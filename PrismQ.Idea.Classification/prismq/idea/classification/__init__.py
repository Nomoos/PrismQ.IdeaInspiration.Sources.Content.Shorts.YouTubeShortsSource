"""Platform-agnostic content classification for PrismQ Idea Sources.

This module provides reusable content classifiers that work across all
PrismQ Idea Source modules in the taxonomy.

Classifiers:
    - StoryDetector: Identifies story-based content (narratives, experiences, confessions)

Compatible with all PrismQ content sources:
- Content.Shorts (YouTube, TikTok, Instagram Reels)
- Content.Streams (Twitch Clips, Kick Clips)
- Content.Forums (Reddit, HackerNews)
- Content.Articles (Medium, Web Articles)
- Content.Podcasts (Spotify, Apple Podcasts)
- Signals.* (Trends, Hashtags, Memes, Challenges, etc.)
- Commerce, Events, Community, Creative, Internal sources
"""

from .story_detector import StoryDetector

__version__ = "1.0.0"
__all__ = ['StoryDetector']
