# Copilot Instructions for PrismQ.IdeaCollector

This file provides guidance for GitHub Copilot and developers on how to build, test, and run the PrismQ.IdeaCollector project.

## Project Overview

PrismQ.IdeaCollector is a Python CLI tool that scrapes idea inspirations from multiple sources (YouTube Shorts, Reddit) and stores them in a SQLite database.

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/PrismQDev/PrismQ.IdeaCollector.git
cd PrismQ.IdeaCollector

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API credentials
```

## Building the Project

This is a Python CLI application and doesn't require compilation. Install in editable mode for development:

```bash
pip install -e .
```

## Running the Application

### Using Python Module

```bash
# Scrape from all sources
python -m idea_collector.cli scrape

# Scrape from specific source
python -m idea_collector.cli scrape --source reddit
python -m idea_collector.cli scrape --source youtube

# List collected ideas
python -m idea_collector.cli list

# View statistics
python -m idea_collector.cli stats

# Clear database
python -m idea_collector.cli clear
```

### Using Quick Start Scripts

```bash
# Run setup script (first time)
./scripts/setup.sh       # Linux/Mac
scripts\setup.bat        # Windows

# Run quickstart demo
./scripts/quickstart.sh  # Linux/Mac
scripts\quickstart.bat   # Windows
```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=idea_collector --cov-report=html

# Run specific test file
pytest tests/test_database.py

# Run specific test
pytest tests/test_database.py::test_function_name
```

### Test Structure

- Tests are located in `tests/` directory
- Test files follow the pattern `test_*.py`
- Use pytest fixtures for setup/teardown
- Mock external API calls to avoid rate limits

## Linting and Code Quality

```bash
# Run flake8 (if configured)
flake8 idea_collector/

# Run black for formatting (if configured)
black idea_collector/ tests/

# Type checking with mypy (if configured)
mypy idea_collector/
```

## Project Structure

```
PrismQ.IdeaCollector/
├── idea_collector/         # Main application code
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   ├── metrics.py          # Universal metrics system
│   ├── scoring/            # Scoring engine
│   └── sources/            # Source plugins
│       ├── __init__.py     # Base plugin interface
│       ├── reddit_plugin.py
│       └── youtube_plugin.py
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Setup scripts
├── issues/                 # File-based issue tracking
│   ├── new/                # Newly reported issues
│   ├── in-progress/        # Issues being worked on
│   ├── review/             # Issues awaiting review
│   ├── blocked/            # Blocked issues
│   └── done/               # Completed issues
└── .github/                # GitHub configuration
```

## Coding Conventions

### Python Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep functions focused and concise (< 50 lines)
- Use meaningful variable names

### Example Function Structure

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

- Keep source plugins in `idea_collector/sources/`
- Add tests in `tests/` with `test_` prefix
- Update configuration in `idea_collector/config.py`
- CLI commands in `idea_collector/cli.py`

## Adding New Features

### Adding a New Source Plugin

1. Create a new file in `idea_collector/sources/` (e.g., `tiktok_plugin.py`)
2. Inherit from the base plugin interface in `sources/__init__.py`
3. Implement the `scrape()` method
4. Add factory method to `UniversalMetrics` in `idea_collector/metrics.py`
5. Register the plugin in `idea_collector/config.py`
6. Add tests in `tests/test_sources.py`
7. Update documentation in `docs/`

## Issue Tracking

### File-Based Issue System

Issues are tracked using markdown files in `issues/` directory, organized by state:

- `issues/new/` - Newly reported issues
- `issues/in-progress/` - Issues currently being worked on
- `issues/review/` - Issues awaiting review
- `issues/blocked/` - Issues that are blocked
- `issues/done/` - Completed issues

### Issue File Format

Each issue is a markdown file with:

```markdown
# Title of the Issue

## Description
Detailed description of the issue or feature request.

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. Expected vs actual behavior

## Notes
- Any additional context
- Related issues or discussions

## Links
- PR: #123
- Commit: abc1234
```

### Moving Issues Between States

Move issue files between state folders as work progresses:

```bash
# Start working on an issue
git mv issues/new/feature-name.md issues/in-progress/feature-name.md

# Move to review
git mv issues/in-progress/feature-name.md issues/review/feature-name.md

# Complete the issue
git mv issues/review/feature-name.md issues/done/feature-name.md
```

## Common Development Tasks

### Debug Configuration Issues

```bash
# Check environment configuration
python -c "from idea_collector.config import Config; c = Config(); print(c.__dict__)"

# Test database connection
python -c "from idea_collector.database import Database; db = Database(':memory:'); print('OK')"
```

### Reset Database

```bash
# Delete the database file
rm ideas.db

# Or use the CLI
python -m idea_collector.cli clear
```

### Update Dependencies

```bash
# Update requirements.txt after adding new packages
pip freeze > requirements.txt

# Or manually edit requirements.txt with version constraints
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Run from project root, ensure virtual environment is activated
2. **API Rate Limits**: Reduce `MAX_RESULTS` in `.env` or add delays between requests
3. **Database Locked**: Close all connections to the database file
4. **Import Errors**: Reinstall in editable mode: `pip install -e .`

### Getting Help

- Check [docs/](../docs/) for detailed documentation
- Review [issues/](../issues/) for known issues
- See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for contribution guidelines

## CI/CD (Future)

When CI/CD is configured, the following will run automatically:

- Linting (flake8, black)
- Type checking (mypy)
- Unit tests (pytest)
- Coverage reports
- Security scanning

## Resources

- [Main README](../README.md)
- [Contributing Guidelines](../docs/CONTRIBUTING.md)
- [Metrics Documentation](../docs/METRICS.md)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
