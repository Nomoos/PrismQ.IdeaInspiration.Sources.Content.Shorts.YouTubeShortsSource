"""Story detection classifier for identifying story-based content across platforms.

This module provides platform-agnostic functionality to detect if content is likely
a story based on its metadata. Designed to work across the PrismQ Idea Sources taxonomy.

Compatible with all PrismQ content sources:
    - Content.Shorts: YouTube Shorts, TikTok, Instagram Reels
    - Content.Streams: Twitch Clips, Kick Clips
    - Content.Forums: Reddit posts, HackerNews threads
    - Content.Articles: Medium posts, Web Articles
    - Content.Podcasts: Spotify episodes, Apple Podcasts
    - And any other content type with text metadata

The classifier uses weighted keyword analysis across title, description, tags,
and subtitles/transcript to identify narrative content including:
    - Personal experiences and real-life stories
    - Reddit-style stories (AITA, TIFU, confessions)
    - Drama narratives and relationship stories
    - Experience sharing and life events

Migration Note:
    This module is designed to be extracted into a shared library:
    PrismQ.Shared.Classifiers or PrismQ.Common.ContentClassification
    for use across all PrismQ Idea Sources modules.
"""

from typing import List, Tuple, Dict


class StoryDetector:
    """Detects if content is likely a story based on metadata analysis."""
    
    # Story detection keywords (weighted by importance)
    STORY_TITLE_KEYWORDS = {
        # High confidence indicators (weight: 3)
        'story': 3, 'storytime': 3, 'aita': 3, 'am i the': 3,
        'tifu': 3, 'confession': 3, 'revenge': 3,
        
        # Medium confidence indicators (weight: 2)
        'relationship': 2, 'breakup': 2, 'cheating': 2, 'caught': 2,
        'ex boyfriend': 2, 'ex girlfriend': 2, 'my wife': 2, 'my husband': 2,
        'family drama': 2, 'toxic': 2, 'entitled': 2, 'karen': 2,
        
        # Low confidence indicators (weight: 1)
        'experience': 1, 'happened': 1, 'crazy': 1, 'insane': 1,
        'unbelievable': 1, 'shocking': 1, 'drama': 1, 'betrayed': 1,
    }
    
    STORY_DESCRIPTION_KEYWORDS = [
        'story', 'storytime', 'experience', 'happened to me', 'true story',
        'real story', 'my story', 'i want to share', 'let me tell you',
        'this is about', 'backstory', 'narrative', 'tale',
    ]
    
    STORY_TAGS = [
        'story', 'storytime', 'storytelling', 'true story', 'real story',
        'personal story', 'life story', 'story time', 'aita', 'reddit story',
        'relationship story', 'revenge story', 'confession',
    ]
    
    # Anti-patterns (likely NOT story videos)
    NON_STORY_KEYWORDS = [
        'tutorial', 'how to', 'review', 'unboxing', 'haul', 'vlog',
        'gameplay', 'walkthrough', 'guide', 'tips', 'tricks', 'reaction',
        'news', 'update', 'announcement', 'trailer', 'teaser', 'music video',
        'podcast', 'interview', 'q&a', 'q and a', 'challenge', 'prank',
    ]
    
    def __init__(self, confidence_threshold: float = 0.3):
        """Initialize story detector.
        
        Args:
            confidence_threshold: Minimum confidence score to classify as story (0-1)
        """
        self.confidence_threshold = confidence_threshold
    
    def detect(self, title: str, description: str = "", tags: List[str] = None, 
               subtitle_text: str = "") -> Tuple[bool, float, List[str]]:
        """Detect if content is likely a story.
        
        Args:
            title: Content title
            description: Content description
            tags: List of tags/hashtags
            subtitle_text: Subtitle/caption text
        
        Returns:
            Tuple of (is_story, confidence_score, indicators_found)
            - is_story: True if content is likely a story
            - confidence_score: Score between 0 and 1
            - indicators_found: List of matched story indicators
        """
        score = 0.0
        indicators = []
        tags = tags or []
        
        # Check title for story keywords
        title_lower = title.lower()
        
        # First check for anti-patterns (non-story content)
        for keyword in self.NON_STORY_KEYWORDS:
            if keyword in title_lower:
                # Strong negative signal - likely not a story
                return False, 0.0, [f"non-story keyword: {keyword}"]
        
        # Check title keywords with weights
        title_score = 0
        for keyword, weight in self.STORY_TITLE_KEYWORDS.items():
            if keyword in title_lower:
                title_score += weight
                indicators.append(f"title: {keyword}")
        
        # If we have strong title indicators, boost the score significantly
        if title_score >= 3:  # At least one high-confidence keyword
            score += 0.5
        elif title_score >= 2:  # Medium confidence
            score += 0.3
        elif title_score >= 1:  # Low confidence
            score += 0.15
        
        # Check description
        if description:
            desc_lower = description.lower()
            
            # Check for anti-patterns in description
            anti_pattern_count = sum(1 for keyword in self.NON_STORY_KEYWORDS if keyword in desc_lower)
            if anti_pattern_count >= 2:
                # Multiple anti-patterns in description
                return False, 0.0, [f"non-story keywords in description: {anti_pattern_count}"]
            
            # Check for story keywords in description
            desc_matches = 0
            for keyword in self.STORY_DESCRIPTION_KEYWORDS:
                if keyword in desc_lower:
                    desc_matches += 1
                    indicators.append(f"description: {keyword}")
                    if desc_matches >= 2:  # Stop after 2 matches
                        break
            
            if desc_matches >= 2:
                score += 0.2
            elif desc_matches >= 1:
                score += 0.1
        
        # Check tags
        if tags:
            tags_lower = [tag.lower() for tag in tags]
            tag_matches = 0
            for tag in self.STORY_TAGS:
                if tag in tags_lower:
                    tag_matches += 1
                    indicators.append(f"tag: {tag}")
            
            if tag_matches >= 2:
                score += 0.2
            elif tag_matches >= 1:
                score += 0.1
        
        # Check subtitle text for story patterns (if available)
        if subtitle_text:
            subtitle_lower = subtitle_text.lower()[:500]  # Check first 500 chars
            
            # Story often starts with first-person narrative
            first_person_indicators = [
                'i was', 'i had', 'i went', 'i got', 'i decided', 'i thought',
                'my story', 'this happened', 'so this happened',
            ]
            
            subtitle_matches = 0
            for indicator in first_person_indicators:
                if indicator in subtitle_lower:
                    subtitle_matches += 1
                    indicators.append(f"subtitle: {indicator}")
                    if subtitle_matches >= 2:  # Stop after 2 matches
                        break
            
            if subtitle_matches >= 1:
                score += 0.15
        
        # Normalize confidence to 0-1 range (cap at 1.0)
        confidence = min(score, 1.0)
        
        # Determine if it's a story
        is_story = confidence >= self.confidence_threshold
        
        return is_story, confidence, indicators
    
    def detect_from_metadata(self, metadata: Dict) -> Tuple[bool, float, List[str]]:
        """Detect if content is a story from metadata dictionary.
        
        Args:
            metadata: Dictionary with 'title', 'description', 'tags', 'subtitle_text' keys
        
        Returns:
            Tuple of (is_story, confidence_score, indicators_found)
        """
        return self.detect(
            title=metadata.get('title', ''),
            description=metadata.get('description', ''),
            tags=metadata.get('tags', []),
            subtitle_text=metadata.get('subtitle_text', '')
        )
