"""Story detection module (deprecated - use src.shared.classifiers.story_detector).

This module is maintained for backward compatibility.
Import from src.shared.classifiers.story_detector for new code.

Migration path:
    Old: from src.story_detector import StoryDetector
    New: from src.shared.classifiers import StoryDetector
"""

# Import from shared location for backward compatibility
from src.shared.classifiers.story_detector import StoryDetector

__all__ = ['StoryDetector']

