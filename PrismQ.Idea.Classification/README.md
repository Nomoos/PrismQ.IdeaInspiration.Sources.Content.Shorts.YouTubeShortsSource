# PrismQ.Idea.Classification

**Platform-agnostic content classification for the PrismQ Idea Sources ecosystem**

## Overview

This package provides reusable content classifiers that work across all PrismQ Idea Source modules in the taxonomy. All classifiers are designed to be platform-independent and require only standard text metadata fields.

## Package Structure

```
PrismQ.Idea.Classification/
├── prismq/
│   └── idea/
│       └── classification/
│           ├── __init__.py
│           └── story_detector.py
├── tests/
│   ├── test_story_detector.py
│   └── test_story_detection_integration.py
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Installation

### From Source (Development)

```bash
cd PrismQ.Idea.Classification
pip install -e .
```

### From PyPI (Future)

```bash
pip install prismq-idea-classification
```

## Usage

### Story Detection

The `StoryDetector` identifies story-based content using weighted keyword analysis:

```python
from prismq.idea.classification import StoryDetector

# Initialize detector
detector = StoryDetector(confidence_threshold=0.3)

# Detect if content is a story
is_story, confidence, indicators = detector.detect(
    title="My AITA Story - Was I Wrong?",
    description="This is my true story about what happened last week...",
    tags=['storytime', 'aita', 'confession'],
    subtitle_text="I was at the store when suddenly..."
)

print(f"Is story: {is_story}")
print(f"Confidence: {confidence:.2f}")
print(f"Story indicators: {indicators}")
```

## Compatible with All PrismQ Idea Sources

This package works across the entire PrismQ taxonomy:

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
- **Sounds**: TikTok Sounds, Instagram Audio
- **Locations**: Geo Local Trends
- **News**: Google News, News API

### Other Categories
- Commerce, Events, Community, Creative, Internal sources

## Available Classifiers

### StoryDetector

Identifies narrative content including:
- Personal experiences and real-life stories
- Reddit-style stories (AITA, TIFU, confessions)
- Drama narratives and relationship stories
- Experience sharing and life events

**Features:**
- 100% local processing (no external API calls)
- Zero external costs (no AI service fees)
- Weighted keyword analysis
- Anti-pattern detection (filters tutorials, reviews, etc.)
- Multi-layer analysis (title, description, tags, subtitles)
- Confidence scoring (0-1 scale)
- 96% code coverage with comprehensive tests

**Platform requirements:**
- Minimal: Only requires standard text fields
- No platform-specific dependencies
- Works with any content metadata structure

## Design Principles

1. **Platform Agnostic**: No platform-specific code or dependencies
2. **Minimal Requirements**: Only standard text fields (title, description, tags, subtitles)
3. **Local Processing**: All computation happens locally, no external API calls
4. **Zero Cost**: No external AI service fees
5. **Well Tested**: High test coverage (96%) with realistic examples
6. **High Performance**: Pure Python, optimized for speed
7. **Easy Integration**: Simple import and usage patterns

## Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest

# Run with coverage
pytest --cov=prismq --cov-report=html

# Run specific test file
pytest tests/test_story_detector.py -v
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/Nomoos/PrismQ.Idea.Classification.git
cd PrismQ.Idea.Classification

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Contributing

When adding new classifiers:

1. Follow the platform-agnostic design pattern
2. Require only standard text fields
3. Process locally (no external API calls)
4. Add comprehensive tests (aim for >90% coverage)
5. Document usage across different content types
6. Update this README

## Roadmap

### Future Classifiers

- **GenreClassifier**: Categorize content by genre (educational, entertainment, news, etc.)
- **SentimentClassifier**: Detect positive/negative/neutral sentiment
- **TopicExtractor**: Extract main topics and themes
- **QualityScorer**: Assess content quality indicators
- **ViralityPredictor**: Predict viral potential based on patterns
- **LanguageDetector**: Identify content language
- **AudienceTargeter**: Determine target audience demographics

All future classifiers will follow the same platform-agnostic design principles.

## License

MIT License - See LICENSE file for details

## Links

- **Source Code**: https://github.com/Nomoos/PrismQ.Idea.Classification
- **Documentation**: https://github.com/Nomoos/PrismQ.Idea.Classification/docs
- **Issue Tracker**: https://github.com/Nomoos/PrismQ.Idea.Classification/issues
- **PyPI Package**: https://pypi.org/project/prismq-idea-classification/ (future)

## Related Projects

- [PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource](https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource)
- [PrismQ.Idea.Sources.Content.Forums.RedditSource](https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Forums.RedditSource)
- [StoryGenerator](https://github.com/Nomoos/StoryGenerator)

## Support

For questions, issues, or feature requests, please open an issue on GitHub.
