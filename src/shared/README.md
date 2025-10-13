# PrismQ Shared Components

This directory contains reusable components designed to work across the entire PrismQ Idea Sources ecosystem.

## Structure

```
src/shared/
├── __init__.py
└── classifiers/              # Content classification modules
    ├── __init__.py
    └── story_detector.py     # Story detection classifier
```

## Purpose

These modules are **platform-agnostic** and designed for reuse across all PrismQ Idea Source modules in the taxonomy:

### Content Sources
- `Content.Shorts.*` - YouTube Shorts, TikTok, Instagram Reels
- `Content.Streams.*` - Twitch Clips, Kick Clips  
- `Content.Forums.*` - Reddit, HackerNews
- `Content.Articles.*` - Medium, Web Articles
- `Content.Podcasts.*` - Spotify, Apple Podcasts

### Signal Sources
- `Signals.Trends.*` - Google Trends, Trends Files
- `Signals.Hashtags.*` - TikTok, Instagram
- `Signals.Memes.*` - Meme Tracker, Know Your Meme
- And more...

### Other Categories
- Commerce, Events, Community, Creative, Internal sources

## Available Classifiers

### StoryDetector

Identifies story-based content across any platform using weighted keyword analysis.

**Usage:**
```python
from src.shared.classifiers import StoryDetector

detector = StoryDetector(confidence_threshold=0.3)
is_story, confidence, indicators = detector.detect(
    title="My AITA Story",
    description="This happened to me last week...",
    tags=['storytime', 'reddit', 'confession'],
    subtitle_text="I was at the store when..."
)

print(f"Is story: {is_story}")
print(f"Confidence: {confidence:.2f}")
print(f"Indicators: {indicators}")
```

**Supported Content Types:**
- Personal narratives and experiences
- Reddit-style stories (AITA, TIFU, confessions)
- Drama and relationship stories
- Real-life event sharing

**Anti-patterns (Automatically Filtered):**
- Tutorials and how-to guides
- Product reviews and unboxings
- Gameplay and walkthroughs
- News updates and announcements

## Design Principles

1. **Platform Agnostic**: No platform-specific dependencies
2. **Minimal Requirements**: Only standard text fields needed
3. **High Performance**: Pure Python, no external API calls
4. **Well Tested**: 96% code coverage with comprehensive tests
5. **Zero Cost**: No external AI service fees

## Migration Path

These components are designed to eventually be extracted into a shared PrismQ library:

**Option 1: PrismQ.Shared**
```python
from prismq.shared.classifiers import StoryDetector
```

**Option 2: PrismQ.Common**
```python
from prismq.common.content_classification import StoryDetector
```

See [MIGRATION_SHARED_CLASSIFIERS.md](../../docs/MIGRATION_SHARED_CLASSIFIERS.md) for detailed migration guide.

## Testing

All shared components have comprehensive test coverage:

```bash
# Test story detector
pytest tests/test_story_detector.py -v

# Test integration with realistic examples
pytest tests/test_story_detection_integration.py -v
```

## Contributing

When adding new shared components:

1. Ensure platform-agnostic design
2. Add comprehensive tests (aim for >90% coverage)
3. Document usage across different content types
4. Follow existing patterns for consistency
5. Update this README with new components

## Future Components

Planned additions to shared classifiers:

- **GenreClassifier**: Categorize by genre (educational, entertainment, etc.)
- **SentimentClassifier**: Positive/negative/neutral sentiment detection
- **TopicExtractor**: Main topic and theme extraction
- **QualityScorer**: Content quality assessment
- **ViralityPredictor**: Viral potential prediction

All will follow the platform-agnostic design pattern.
