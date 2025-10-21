# Contributing to PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource

Thank you for your interest in contributing to this PrismQ module!

## Development Environment

### System Requirements

- **Operating System**: Windows (primary), Linux (development only)
- **GPU**: NVIDIA RTX 5090 (32GB VRAM)
- **CPU**: AMD Ryzen processor (multi-core)
- **RAM**: 64GB DDR5
- **Python**: 3.10 or higher

> **Note**: While development on Linux is supported, the primary target platform is Windows with high-end hardware for AI workloads.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Adding New Source Plugins](#adding-new-source-plugins)

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (OS, Python version, GPU/CPU specs)
- Error logs or screenshots if applicable

Use the bug report template provided in the issue tracker.

### Suggesting Features

Feature suggestions are welcome! Please use the feature request template and include:

- A clear description of the feature
- Why this feature would be useful
- Any alternative solutions you've considered
- Whether you're willing to work on implementing it
- Hardware/platform considerations

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure nothing breaks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.10 or higher (required)
- pip package manager
- Virtual environment (recommended)
- Windows OS (recommended)
- NVIDIA GPU with CUDA support (optional, for future AI features)

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource.git
   cd PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows (primary platform)
   venv\Scripts\activate
   
   # On Linux (development only)
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install development dependencies
   ```

4. Set up configuration:
   ```bash
   # On Windows
   copy .env.example .env
   
   # On Linux
   cp .env.example .env
   
   # Edit .env with your API credentials
   ```

5. Run tests:
   ```bash
   pytest
   ```

## Pull Request Process

1. **Update Documentation**: Ensure README.md and any relevant documentation is updated with details of changes
2. **Update Tests**: Add or update tests for your changes
3. **Follow Code Standards**: Ensure your code follows the project's coding standards
4. **Update CHANGELOG**: Add an entry to CHANGELOG.md describing your changes
5. **Small PRs**: Keep pull requests focused on a single feature or fix
6. **Descriptive Commits**: Write clear, descriptive commit messages
7. **Fill PR Template**: Complete the pull request template with all relevant information

### PR Review Process

- PRs require review from at least one maintainer
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Add docstrings to all public functions and classes using Google style
- Keep functions small and focused (< 50 lines)
- Write meaningful commit messages

### Performance Considerations

- Optimize for potential GPU utilization on RTX 5090 (future features)
- Consider memory constraints (32GB VRAM, 64GB RAM)
- Use batch processing where applicable
- Test on the target platform when possible

### Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting PR
- Aim for high test coverage (>80%)
- Test on Windows platform when possible

### Example Code Style

```python
def scrape(self) -> List[Dict[str, Any]]:
    """Scrape ideas from the source.
    
    Returns:
        List of idea dictionaries with keys:
            - source_id: Unique identifier from source
            - title: Idea title
            - description: Idea description
            - tags: Tags or categories
            - metrics: Dictionary of metrics
    """
    pass
```

### File Organization

- Keep source plugins in `mod/sources/`
- Add tests in `tests/` with `test_` prefix
- Update configuration in `mod/config.py`
- CLI commands in `mod/cli.py`

## Enhancing YouTube Shorts Functionality

This repository focuses specifically on YouTube Shorts scraping. To enhance functionality:

1. Update the YouTube plugin in `mod/sources/youtube_plugin.py`

2. Example enhancement:
   ```python
   from . import SourcePlugin
   from ..metrics import UniversalMetrics
   
   class YouTubePlugin(SourcePlugin):
       def get_source_name(self) -> str:
           return "youtube"
       
       def scrape(self) -> List[Dict[str, Any]]:
           # Enhance scraping logic
           pass
   ```

3. Update `UniversalMetrics` factory method in `mod/metrics.py` if needed:
   ```python
   @classmethod
   def from_youtube(cls, video_data: Dict[str, Any]) -> 'UniversalMetrics':
       # Enhance metric mapping
       pass
   ```

4. Update configuration in `.env.example` if new settings are needed

5. Add tests for the enhancements in `tests/`

6. Update documentation:
   - Update README.md features list
   - Document new metrics in METRICS.md
   - Add usage examples

## Adding Support for Other Platforms

To add support for other platforms (TikTok, Instagram Reels, etc.), create a new repository following the PrismQ Idea Sources taxonomy:
- `PrismQ.IdeaInspiration.Sources.Content.Shorts.TikTokSource`
- `PrismQ.IdeaInspiration.Sources.Content.Shorts.InstagramReelsSource`
- etc.

See the [PrismQ.RepositoryTemplate](https://github.com/Nomoos/PrismQ.RepositoryTemplate) for module structure guidelines.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_database.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Mock external API calls
- Test both success and failure cases

Example:
```python
def test_database_stores_idea():
    """Test that database correctly stores an idea."""
    db = Database(":memory:")
    idea = {
        "source": "test",
        "source_id": "123",
        "title": "Test Idea"
    }
    db.store_idea(idea)
    ideas = db.get_all_ideas()
    assert len(ideas) == 1
    assert ideas[0]["title"] == "Test Idea"
```

## Questions?

If you have questions about contributing, please:
- Check the [README.md](../README.md) for general documentation
- Open a discussion in the GitHub Discussions tab
- Reach out to the maintainers

Thank you for contributing to PrismQ.IdeaInspiration.Sources.Content.Shorts.YouTubeShortsSource! 🎉
