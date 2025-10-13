"""Story detection module (deprecated - use prismq.idea.classification).

This module is maintained for backward compatibility.
Import from prismq.idea.classification for new code.

Migration path:
    Old: from src.story_detector import StoryDetector
    Old: from src.shared.classifiers import StoryDetector
    New: from prismq.idea.classification import StoryDetector

Note: The PrismQ.Idea.Classification package in the top-level directory
is ready for extraction as a standalone package.
"""

# Import from shared location for backward compatibility
from src.shared.classifiers.story_detector import StoryDetector

__all__ = ['StoryDetector']

