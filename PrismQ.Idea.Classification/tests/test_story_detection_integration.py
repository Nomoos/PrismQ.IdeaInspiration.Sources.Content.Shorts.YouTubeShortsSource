"""Integration tests for story detection with real video examples."""

import pytest
from prismq.idea.classification import StoryDetector


class TestStoryDetectionIntegration:
    """Integration tests for story detection with realistic video data."""
    
    def test_story_detection_with_story_videos(self):
        """Test story detection with a list of story videos."""
        detector = StoryDetector()
        
        # Realistic examples of story videos
        story_videos = [
            {
                'title': 'My AITA Story - I Kicked My Sister Out',
                'description': 'This is my true story about what happened last week when my sister came to visit.',
                'tags': ['storytime', 'aita', 'family drama'],
                'subtitle_text': 'So this happened to me yesterday. I was sitting at home when...'
            },
            {
                'title': 'TIFU by accidentally proposing to my roommate',
                'description': 'Let me tell you about the most embarrassing experience of my life.',
                'tags': ['tifu', 'reddit story', 'confession'],
                'subtitle_text': 'I thought it would be funny but I had no idea what would happen next.'
            },
            {
                'title': 'My Toxic Relationship Story - How I Escaped',
                'description': 'Sharing my personal story about getting out of a bad relationship.',
                'tags': ['relationship story', 'true story', 'personal story'],
                'subtitle_text': 'I was trapped for years before I finally decided to leave.'
            },
            {
                'title': 'Revenge on My Cheating Ex',
                'description': 'This is the story of how I got back at my ex boyfriend.',
                'tags': ['revenge story', 'storytime'],
                'subtitle_text': 'I caught him cheating and decided to do something about it.'
            },
            {
                'title': 'Storytime: The Craziest Thing That Ever Happened To Me',
                'description': 'You won\'t believe this happened to me. True story!',
                'tags': ['story time', 'crazy experience'],
                'subtitle_text': 'I was walking down the street when suddenly...'
            }
        ]
        
        results = []
        for video in story_videos:
            is_story, confidence, indicators = detector.detect(
                title=video['title'],
                description=video['description'],
                tags=video['tags'],
                subtitle_text=video['subtitle_text']
            )
            results.append({
                'title': video['title'],
                'is_story': is_story,
                'confidence': confidence,
                'indicators': indicators
            })
        
        # All should be detected as stories
        for result in results:
            assert result['is_story'] is True, f"Failed to detect story: {result['title']}"
            assert result['confidence'] >= 0.3, f"Low confidence for story: {result['title']}"
            assert len(result['indicators']) > 0, f"No indicators found for: {result['title']}"
        
        # Verify we detected all 5 as stories
        story_count = sum(1 for r in results if r['is_story'])
        assert story_count == 5, f"Expected 5 stories, got {story_count}"
    
    def test_story_detection_with_non_story_videos(self):
        """Test story detection with a list of non-story videos."""
        detector = StoryDetector()
        
        # Realistic examples of non-story videos
        non_story_videos = [
            {
                'title': 'How to Make Amazing YouTube Shorts - Tutorial',
                'description': 'Learn how to create viral shorts with this step-by-step guide.',
                'tags': ['tutorial', 'how to', 'youtube tips'],
                'subtitle_text': 'First, you need to open your video editor and...'
            },
            {
                'title': 'iPhone 15 Pro Review - Is It Worth It?',
                'description': 'My honest review of the new iPhone 15 Pro after 2 weeks.',
                'tags': ['review', 'tech', 'iphone'],
                'subtitle_text': 'The camera quality is impressive but the price is high...'
            },
            {
                'title': 'Epic Fortnite Gameplay Highlights',
                'description': 'Check out my best gameplay moments from this week.',
                'tags': ['gameplay', 'gaming', 'fortnite'],
                'subtitle_text': 'Watch as I get this insane victory royale...'
            },
            {
                'title': 'Unboxing the New PS5',
                'description': 'Opening up the PlayStation 5 and showing what\'s inside.',
                'tags': ['unboxing', 'playstation', 'gaming'],
                'subtitle_text': 'Let\'s see what comes in the box...'
            },
            {
                'title': 'Daily Vlog - A Day in My Life',
                'description': 'Follow me around for a typical day.',
                'tags': ['vlog', 'daily vlog', 'lifestyle'],
                'subtitle_text': 'Good morning everyone, today we\'re going to...'
            }
        ]
        
        results = []
        for video in non_story_videos:
            is_story, confidence, indicators = detector.detect(
                title=video['title'],
                description=video['description'],
                tags=video['tags'],
                subtitle_text=video['subtitle_text']
            )
            results.append({
                'title': video['title'],
                'is_story': is_story,
                'confidence': confidence,
                'indicators': indicators
            })
        
        # All should be detected as non-stories
        for result in results:
            assert result['is_story'] is False, f"Incorrectly detected as story: {result['title']}"
            assert result['confidence'] == 0.0, f"Non-zero confidence for non-story: {result['title']}"
        
        # Verify we detected all 5 as non-stories
        non_story_count = sum(1 for r in results if not r['is_story'])
        assert non_story_count == 5, f"Expected 5 non-stories, got {non_story_count}"
    
    def test_story_detection_with_mixed_videos(self):
        """Test story detection with a mixed list of story and non-story videos."""
        detector = StoryDetector()
        
        # Mixed examples
        videos = [
            # Story videos (should be True)
            {
                'title': 'My Confession: I Stole From My Best Friend',
                'description': 'True story about a mistake I made.',
                'tags': ['confession', 'true story'],
                'subtitle_text': 'I need to tell you what I did.',
                'expected': True
            },
            {
                'title': 'AITA for not inviting my mom to my wedding?',
                'description': 'Let me explain the situation.',
                'tags': ['aita', 'reddit'],
                'subtitle_text': 'So here\'s what happened...',
                'expected': True
            },
            # Non-story videos (should be False)
            {
                'title': 'Top 10 Tips for Better Videos',
                'description': 'Tips and tricks for content creators.',
                'tags': ['tips', 'tutorial', 'guide'],
                'subtitle_text': 'Here are my top recommendations...',
                'expected': False
            },
            {
                'title': 'React to Viral TikTok',
                'description': 'Watching and reacting to trending content.',
                'tags': ['reaction', 'tiktok'],
                'subtitle_text': 'Oh my god, did you see that?',
                'expected': False
            },
            # Ambiguous (medium confidence)
            {
                'title': 'My Experience with Online Dating',
                'description': 'This is my story about what happened to me.',
                'tags': ['dating', 'experience'],
                'subtitle_text': 'Online dating has been interesting for me.',
                'expected': True  # Should detect due to "experience" + description keywords
            }
        ]
        
        results = []
        for video in videos:
            is_story, confidence, indicators = detector.detect(
                title=video['title'],
                description=video['description'],
                tags=video['tags'],
                subtitle_text=video['subtitle_text']
            )
            results.append({
                'title': video['title'],
                'is_story': is_story,
                'confidence': confidence,
                'expected': video['expected']
            })
        
        # Check each result matches expectation
        for result in results:
            assert result['is_story'] == result['expected'], \
                f"Detection mismatch for '{result['title']}': expected {result['expected']}, got {result['is_story']}"
        
        # Verify counts
        story_count = sum(1 for r in results if r['is_story'])
        expected_story_count = sum(1 for v in videos if v['expected'])
        assert story_count == expected_story_count, \
            f"Expected {expected_story_count} stories, got {story_count}"
    
    def test_story_detection_confidence_levels(self):
        """Test that confidence levels vary appropriately."""
        detector = StoryDetector()
        
        videos = [
            {
                'title': 'AITA Storytime Confession Revenge',  # Multiple high-weight keywords
                'description': 'This is my true story that happened to me.',
                'tags': ['storytime', 'aita', 'confession'],
                'subtitle_text': 'I was shocked when this happened.',
                'min_confidence': 0.8  # Expect very high confidence
            },
            {
                'title': 'My Experience',  # Single low-weight keyword
                'description': '',
                'tags': [],
                'subtitle_text': '',
                'min_confidence': 0.15,  # Expect low but non-zero confidence
                'max_confidence': 0.25
            },
            {
                'title': 'Tutorial: How to Code',  # Anti-pattern
                'description': 'Learn programming step by step.',
                'tags': ['tutorial'],
                'subtitle_text': '',
                'min_confidence': 0.0,  # Expect zero confidence
                'max_confidence': 0.0
            }
        ]
        
        for video in videos:
            is_story, confidence, indicators = detector.detect(
                title=video['title'],
                description=video['description'],
                tags=video['tags'],
                subtitle_text=video['subtitle_text']
            )
            
            min_conf = video.get('min_confidence', 0)
            max_conf = video.get('max_confidence', 1.0)
            
            assert confidence >= min_conf, \
                f"Confidence too low for '{video['title']}': {confidence} < {min_conf}"
            assert confidence <= max_conf, \
                f"Confidence too high for '{video['title']}': {confidence} > {max_conf}"
    
    def test_story_detection_batch_processing(self):
        """Test processing a batch of videos efficiently."""
        detector = StoryDetector()
        
        # Simulate batch of videos
        video_batch = [
            {'title': f'Story #{i}', 'description': 'My storytime experience', 'tags': ['story'], 'subtitle_text': ''}
            for i in range(10)
        ] + [
            {'title': f'Tutorial #{i}', 'description': 'How to guide', 'tags': ['tutorial'], 'subtitle_text': ''}
            for i in range(10)
        ]
        
        # Process all videos
        story_results = []
        for video in video_batch:
            is_story, confidence, indicators = detector.detect(
                title=video['title'],
                description=video['description'],
                tags=video['tags'],
                subtitle_text=video['subtitle_text']
            )
            story_results.append(is_story)
        
        # Verify we got expected counts
        story_count = sum(story_results)
        assert story_count == 10, f"Expected 10 stories, got {story_count}"
        
        non_story_count = len(story_results) - story_count
        assert non_story_count == 10, f"Expected 10 non-stories, got {non_story_count}"
