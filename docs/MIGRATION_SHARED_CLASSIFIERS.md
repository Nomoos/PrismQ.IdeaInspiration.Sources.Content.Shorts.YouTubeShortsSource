# Migration Guide: Shared Classifiers

## Overview

The `StoryDetector` classifier has been reorganized into a shared module structure to facilitate reuse across the PrismQ Idea Sources ecosystem.

## New Structure

```
src/
├── shared/                          # Shared components for PrismQ ecosystem
│   ├── __init__.py
│   └── classifiers/                 # Content classifiers
│       ├── __init__.py
│       └── story_detector.py        # Platform-agnostic story detection
├── sources/                         # YouTube-specific source plugins
│   ├── youtube_channel_plugin.py
│   ├── youtube_trending_plugin.py
│   └── youtube_plugin.py
└── story_detector.py                # Backward compatibility wrapper (deprecated)
```

## PrismQ Taxonomy Integration

The shared classifiers are designed to work across the entire PrismQ Idea Sources taxonomy:

### Content Sources
- **Shorts**: YouTube, TikTok, Instagram Reels
- **Streams**: Twitch Clips, Kick Clips
- **Forums**: Reddit, HackerNews
- **Articles**: Medium, Web Articles
- **Podcasts**: Spotify, Apple Podcasts

### Signal Sources
- **Trends**: Google Trends, Trends Files
- **Hashtags**: TikTok, Instagram
- **Memes**: Meme Tracker, Know Your Meme
- **Challenges**: Social Challenges
- **Sounds**: TikTok Sounds, Instagram Audio Trends
- **Locations**: Geo Local Trends
- **News**: Google News, News API

### Other Categories
- **Commerce**: Amazon, Etsy, App Store
- **Events**: Calendar, Sports, Entertainment
- **Community**: QA, Comments, Feedback, Prompts
- **Creative**: Lyrics, Scripts, Moodboards
- **Internal**: Manual, CSV Import

## Usage in This Module

### Current (Backward Compatible)
```python
from src.story_detector import StoryDetector

detector = StoryDetector()
is_story, confidence, indicators = detector.detect(
    title="My AITA Story",
    description="This happened to me...",
    tags=['storytime', 'reddit'],
    subtitle_text="I was at the store when..."
)
```

### Recommended (New Location)
```python
from src.shared.classifiers import StoryDetector

detector = StoryDetector()
is_story, confidence, indicators = detector.detect(
    title="My AITA Story",
    description="This happened to me...",
    tags=['storytime', 'reddit'],
    subtitle_text="I was at the store when..."
)
```

## Migration to Shared Library

When ready to extract to a shared PrismQ library, the structure would be:

### Option 1: PrismQ.Shared Package
```
PrismQ.Shared/
├── classifiers/
│   ├── __init__.py
│   └── story_detector.py
├── metrics/
│   └── universal_metrics.py
└── utils/
    └── text_processing.py
```

Usage across modules:
```python
# In any PrismQ Idea Source module
from prismq.shared.classifiers import StoryDetector
```

### Option 2: PrismQ.Common Package
```
PrismQ.Common/
├── content_classification/
│   ├── __init__.py
│   └── story_detector.py
└── metadata/
    └── normalizers.py
```

Usage:
```python
from prismq.common.content_classification import StoryDetector
```

## Advantages of Shared Structure

1. **Reusability**: Same classifier works across YouTube, TikTok, Instagram, Reddit, etc.
2. **Consistency**: Unified story detection logic across all platforms
3. **Maintainability**: Update once, benefits all modules
4. **Testing**: Shared test suite validates behavior for all use cases
5. **Performance**: No code duplication, single implementation

## Migration Checklist

When extracting to a shared library:

- [ ] Create `PrismQ.Shared` or `PrismQ.Common` package
- [ ] Copy `src/shared/classifiers/` to the new package
- [ ] Update imports in all PrismQ modules
- [ ] Update tests to use new import paths
- [ ] Add dependency in each module's `requirements.txt`
- [ ] Update documentation across all modules
- [ ] Deprecate old import paths with warnings
- [ ] Remove deprecated code after migration period

## Testing Across Platforms

The classifier is designed to work with any content metadata:

```python
# YouTube Short
detector.detect(
    title="My Story Time",
    description="Let me tell you what happened",
    tags=['story', 'experience'],
    subtitle_text="I was walking home when..."
)

# Reddit Post
detector.detect(
    title="AITA for not inviting my mom?",
    description="Here's the situation...",
    tags=['aita', 'family'],
    subtitle_text=""
)

# TikTok Video
detector.detect(
    title="Storytime: The Craziest Date",
    description="#storytime #dating",
    tags=['storytime', 'dating'],
    subtitle_text="So this guy showed up and..."
)

# Medium Article
detector.detect(
    title="My Experience with Remote Work",
    description="A personal story about...",
    tags=['experience', 'work'],
    subtitle_text=""
)
```

## Platform-Agnostic Design

The classifier only requires standard text fields:
- `title`: Content title/headline
- `description`: Content description/body preview
- `tags`: List of tags/hashtags/categories
- `subtitle_text`: Subtitles/transcript/captions (optional)

No platform-specific dependencies or assumptions.

## Future Enhancements

Potential additions to shared classifiers:

1. **GenreClassifier**: Categorize content by genre (educational, entertainment, news, etc.)
2. **SentimentClassifier**: Detect positive/negative/neutral sentiment
3. **TopicExtractor**: Extract main topics and themes
4. **QualityScorer**: Assess content quality indicators
5. **ViralityPredictor**: Predict viral potential based on patterns

All classifiers would follow the same platform-agnostic design pattern.
