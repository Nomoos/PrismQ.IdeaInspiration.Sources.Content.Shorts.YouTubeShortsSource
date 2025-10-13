# Migration Guide: PrismQ.Idea.Classification

This guide explains how to extract `PrismQ.Idea.Classification` as a standalone package and integrate it into PrismQ Idea Sources modules.

## Overview

`PrismQ.Idea.Classification` provides platform-agnostic content classifiers that work across all PrismQ Idea Source modules. This package is designed to be installable via pip and imported using the namespace package pattern.

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
├── LICENSE
├── MANIFEST.in
└── MIGRATION_GUIDE.md
```

## Extracting as Standalone Repository

### Step 1: Create New Repository

```bash
# On GitHub, create new repository: PrismQ.Idea.Classification

# Clone the new repository
git clone https://github.com/Nomoos/PrismQ.Idea.Classification.git
cd PrismQ.Idea.Classification
```

### Step 2: Copy Package Contents

Copy the entire `PrismQ.Idea.Classification/` folder contents to the new repository:

```bash
# From the YouTubeShortsSource repository
cp -r PrismQ.Idea.Classification/* /path/to/new/PrismQ.Idea.Classification/
```

### Step 3: Initialize Git

```bash
cd /path/to/new/PrismQ.Idea.Classification
git add .
git commit -m "Initial commit: PrismQ.Idea.Classification package"
git push origin main
```

### Step 4: Publish to PyPI (Optional)

```bash
# Build the package
python setup.py sdist bdist_wheel

# Upload to PyPI (requires PyPI account)
twine upload dist/*
```

## Using in PrismQ Idea Sources Modules

### Installation

Add to `requirements.txt` in any PrismQ Idea Sources module:

```txt
# For local development (editable install)
-e /path/to/PrismQ.Idea.Classification

# For production (from PyPI - future)
prismq-idea-classification>=1.0.0
```

### Import Usage

Update imports in your code:

**Old (module-specific):**
```python
from src.story_detector import StoryDetector
from src.shared.classifiers import StoryDetector
```

**New (namespace package):**
```python
from prismq.idea.classification import StoryDetector
```

### Example Integration

In `PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource`:

```python
# src/sources/youtube_channel_plugin.py
from prismq.idea.classification import StoryDetector

class YouTubeChannelPlugin(SourcePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.story_detector = StoryDetector()
        # ... rest of initialization
```

## Backward Compatibility

To maintain backward compatibility in existing modules, create a wrapper:

```python
# src/story_detector.py
"""Backward compatibility wrapper (deprecated)."""
from prismq.idea.classification import StoryDetector
__all__ = ['StoryDetector']
```

This allows existing code to continue working while migrating to the new import path.

## Testing After Migration

Run tests to ensure everything works:

```bash
# In the classification package
cd PrismQ.Idea.Classification
pytest tests/ -v

# In each source module
cd PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource
pytest tests/test_story_detector.py -v
```

## Integration Checklist

When integrating into a new PrismQ Idea Sources module:

- [ ] Add `prismq-idea-classification` to `requirements.txt`
- [ ] Update imports to use `from prismq.idea.classification import ...`
- [ ] Remove local copies of classifier code
- [ ] Run tests to verify integration
- [ ] Update documentation with new import paths
- [ ] Remove deprecated wrappers after migration period

## Namespace Package Pattern

PrismQ uses namespace packages to organize related modules:

```
prismq/
├── idea/
│   ├── classification/        # This package
│   │   └── story_detector.py
│   └── sources/               # Source modules (future)
│       ├── content/
│       │   ├── shorts/
│       │   │   ├── youtube/
│       │   │   ├── tiktok/
│       │   │   └── instagram/
│       │   └── forums/
│       │       └── reddit/
│       └── signals/
│           └── trends/
└── other/                     # Other PrismQ packages
```

This allows:
- Clean imports: `from prismq.idea.classification import StoryDetector`
- Independent versioning of each package
- Shared namespace across repositories
- Easy discoverability

## Advantages of Extraction

1. **Reusability**: Single package used by all PrismQ modules
2. **Maintainability**: Update once, benefits all modules
3. **Testing**: Comprehensive tests in one location
4. **Versioning**: Independent version control
5. **Distribution**: Easy installation via pip
6. **Documentation**: Centralized documentation
7. **Contribution**: Easier for community contributions

## Development Workflow

### Making Changes

1. Make changes in `PrismQ.Idea.Classification` repository
2. Test locally:
   ```bash
   pytest tests/ -v
   ```
3. Create PR and merge
4. Update version in `setup.py`
5. Tag release:
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
6. Update `requirements.txt` in dependent modules:
   ```txt
   prismq-idea-classification>=1.0.1
   ```

### Local Development

For local development across multiple modules:

```bash
# In classification package
cd PrismQ.Idea.Classification
pip install -e .

# In source modules
cd ../PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource
pip install -e ../PrismQ.Idea.Classification
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'prismq'`:

```bash
# Ensure package is installed
pip install -e /path/to/PrismQ.Idea.Classification

# Verify installation
python -c "from prismq.idea.classification import StoryDetector; print('OK')"
```

### Namespace Package Issues

If namespace packages don't resolve correctly:

1. Ensure `__init__.py` files use `pkgutil.extend_path`
2. Don't use `__init__.py` as regular packages
3. Install in editable mode for development

### Test Failures

If tests fail after migration:

1. Check import paths are updated
2. Verify package is installed correctly
3. Run tests with verbose output: `pytest -vv`

## Support

For issues with migration:
- Open issue in the classification package repository
- Check documentation in README.md
- Review example integrations in source modules

## Future Enhancements

Additional classifiers to add:

- GenreClassifier
- SentimentClassifier
- TopicExtractor
- QualityScorer
- ViralityPredictor
- LanguageDetector
- AudienceTargeter

Each will follow the same platform-agnostic pattern.
