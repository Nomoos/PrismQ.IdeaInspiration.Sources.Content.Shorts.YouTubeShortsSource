# Contributing to PrismQ.IdeaCollector

Thank you for considering contributing to PrismQ.IdeaCollector! We welcome contributions from the community.

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
- Your environment (OS, Python version, etc.)
- Error logs or screenshots if applicable

Use the bug report template provided in the issue tracker.

### Suggesting Features

Feature suggestions are welcome! Please use the feature request template and include:

- A clear description of the feature
- Why this feature would be useful
- Any alternative solutions you've considered
- Whether you're willing to work on implementing it

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

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/PrismQ.IdeaCollector.git
   cd PrismQ.IdeaCollector
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install development dependencies
   ```

4. Set up configuration:
   ```bash
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
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

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
            - metrics: Dictionary of metrics for scoring
    """
    pass
```

### File Organization

- Keep source plugins in `src/sources/`
- Add tests in `tests/` with `test_` prefix
- Update configuration in `src/config.py`
- CLI commands in `src/cli.py`

## Adding New Source Plugins

To add support for a new platform (e.g., TikTok, Instagram):

1. Create a new file in `src/sources/` (e.g., `tiktok_plugin.py`)

2. Implement the `SourcePlugin` interface:
   ```python
   from . import SourcePlugin
   from ..metrics import UniversalMetrics
   
   class TikTokPlugin(SourcePlugin):
       def get_source_name(self) -> str:
           return "tiktok"
       
       def scrape(self) -> List[Dict[str, Any]]:
           # Implement scraping logic
           pass
   ```

3. Add a factory method to `UniversalMetrics` class in `src/metrics.py`:
   ```python
   @classmethod
   def from_tiktok(cls, video_data: Dict[str, Any]) -> 'UniversalMetrics':
       # Map TikTok data to universal metrics
       pass
   ```

4. Update configuration in `.env.example` with new platform settings

5. Add tests for the new plugin in `tests/test_tiktok_plugin.py`

6. Update documentation:
   - Add platform to README.md features list
   - Document metrics mapping in METRICS.md
   - Add usage examples

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
- Check the [README.md](README.md) for general documentation
- Open a discussion in the GitHub Discussions tab
- Reach out to the maintainers

Thank you for contributing to PrismQ.IdeaCollector! 🎉
