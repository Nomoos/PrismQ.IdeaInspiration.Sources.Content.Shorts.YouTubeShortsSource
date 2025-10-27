"""Processor module for transforming YouTube Shorts data to IdeaInspiration format.

This module provides the IdeaProcessor class for transforming YouTubeShortsSource
database records into the standardized IdeaInspiration model as defined in
PrismQ.IdeaInspiration.Model.
"""

from processor.idea_processor import IdeaProcessor, IdeaInspiration, ContentType

__all__ = ['IdeaProcessor', 'IdeaInspiration', 'ContentType']
