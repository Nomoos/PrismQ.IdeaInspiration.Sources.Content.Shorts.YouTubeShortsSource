# Copilot Instructions for PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource

This file provides guidance for GitHub Copilot and developers on how to build, test, and run the PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource project.

## Project Context

PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource is a specialized PrismQ module for scraping YouTube Shorts content. It's part of the PrismQ Idea Sources ecosystem which includes:
- **PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource** - YouTube Shorts scraping (this module)
- **PrismQ.Idea.Sources.Content.Forums.RedditSource** - Reddit scraping (separate module)
- **StoryGenerator** - Automated story and video generation pipeline
- **PrismQ.RepositoryTemplate** - Standardized template for PrismQ modules
- Other specialized content source modules

## Target Platform

All code should be optimized for:
- **Operating System**: Windows (primary), Linux (development only)
- **GPU**: NVIDIA RTX 5090 (Ada Lovelace architecture, 32GB VRAM)
- **CPU**: AMD Ryzen processor (multi-core)
- **RAM**: 64GB DDR5
- **Python**: 3.10 or higher

## Project Overview

PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource is a Python CLI tool that scrapes idea inspirations from YouTube Shorts and stores them in a SQLite database.

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher (required)
- pip package manager
- Virtual environment (recommended)
- Windows OS (recommended)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource.git
cd PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux (development only)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env  # On Windows
# cp .env.example .env  # On Linux
# Edit .env and add your YouTube API key
```

## Building the Project

This is a Python CLI application and doesn't require compilation. Install in editable mode for development:

```bash
pip install -e .
```

## Running the Application

### Using Python Module

```bash
# Scrape from YouTube Shorts
python -m src.cli scrape

# List collected ideas
python -m src.cli list

# View statistics
python -m src.cli stats

# Clear database
python -m src.cli clear
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
pytest --cov=src --cov-report=html

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
flake8 src/

# Run black for formatting (if configured)
black src/ tests/

# Type checking with mypy (if configured)
mypy src/
```

## Project Structure

```
```
PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource/
├── src/         # Main application code
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   ├── metrics.py          # Universal metrics system
│   ├── scoring/            # Scoring engine
│   └── sources/            # Source plugins
│       ├── __init__.py     # Base plugin interface
│       └── youtube_plugin.py
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Setup scripts
├── issues/                 # File-based issue tracking
│   ├── new/                # Newly reported issues
│   ├── wip/                # Issues being worked on (Work In Progress)
│   └── done/               # Completed issues
└── .github/                # GitHub configuration
```

## Coding Conventions

### Python Style

- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Add docstrings to all public functions and classes using Google style
- Keep functions focused and concise (< 50 lines)
- Use meaningful variable names

### Performance Considerations

- Optimize for potential GPU utilization on RTX 5090 (future features)
- Consider memory constraints (32GB VRAM, 64GB RAM)
- Use batch processing where applicable
- Implement proper resource management for API calls
- Profile performance-critical sections

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

- Keep source plugins in `src/sources/`
- Add tests in `tests/` with `test_` prefix
- Update configuration in `src/config.py`
- CLI commands in `src/cli.py`

## Adding New Features

### Extending YouTube Shorts Functionality

1. Enhance the YouTube plugin in `src/sources/youtube_plugin.py`
2. Update the `scrape()` method to add new capabilities
3. Add any new configuration options to `src/config.py`
4. Add factory method adjustments to `UniversalMetrics` if needed
5. Add tests in `tests/`
6. Update documentation in `docs/`

### Adding Support for Other Platforms

To add support for other content types (TikTok, Instagram Reels, etc.), create a new repository following the PrismQ Idea Sources taxonomy:
- `PrismQ.Idea.Sources.Content.Shorts.TikTokSource`
- `PrismQ.Idea.Sources.Content.Shorts.InstagramReelsSource`
- etc.

See the [PrismQ.RepositoryTemplate](https://github.com/Nomoos/PrismQ.RepositoryTemplate) for structure guidelines.

## Issue Tracking

### File-Based Issue System

Issues are tracked using markdown files in `issues/` directory, organized by state:

- `issues/new/` - Newly reported issues
- `issues/wip/` - Issues currently being worked on (Work In Progress)
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
git mv issues/new/feature-name.md issues/wip/feature-name.md

# Complete the issue
git mv issues/wip/feature-name.md issues/done/feature-name.md
```

## Integration with PrismQ Ecosystem

### Module Compatibility

- Follow consistent naming conventions across PrismQ modules
- Use compatible data formats for inter-module communication
- Document integration points with other PrismQ modules
- Consider pipeline compatibility with StoryGenerator and other modules

### Data Export

- Ensure collected ideas can be easily exported for downstream modules
- Maintain consistent schema for idea metadata
- Support various output formats (JSON, CSV, database)

## AI/ML Considerations

### Future GPU Optimization

When implementing AI-powered features:
- Use mixed precision (FP16/BF16) for RTX 5090
- Implement proper batch sizing for 32GB VRAM
- Consider CUDA/cuDNN compatibility
- Profile GPU memory usage
- Use CUDA graphs for repetitive operations
- Consider model quantization for efficiency

### Dependencies for AI Features

- Prefer well-maintained, GPU-accelerated libraries
- Document version requirements clearly
- Test compatibility with PyTorch/TensorFlow if using deep learning
- Ensure CUDA toolkit version compatibility

## Common Development Tasks

### Debug Configuration Issues

```bash
# Check environment configuration
python -c "from src.config import Config; c = Config(); print(c.__dict__)"

# Test database connection
python -c "from src.database import Database; db = Database(':memory:'); print('OK')"
```

### Reset Database

```bash
# Delete the database file
rm ideas.db

# Or use the CLI
python -m src.cli clear
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
