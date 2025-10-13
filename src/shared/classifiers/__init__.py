"""Content classifiers for PrismQ Idea Sources.

This module provides classifiers that can categorize and filter content
across different platforms and content types in the PrismQ ecosystem.

Classifiers:
    - StoryDetector: Identifies story-based content (narratives, experiences, confessions)
    
These classifiers are platform-agnostic and can be used across:
- Content.Shorts (YouTube, TikTok, Instagram Reels)
- Content.Streams (Twitch Clips, Kick Clips)
- Content.Forums (Reddit, HackerNews)
- Content.Articles (Medium, Web Articles)
- Content.Podcasts (Spotify, Apple Podcasts)
- And any other content source in the PrismQ taxonomy
"""

from .story_detector import StoryDetector

__all__ = ['StoryDetector']
