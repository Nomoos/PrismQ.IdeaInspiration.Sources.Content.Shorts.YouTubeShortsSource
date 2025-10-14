# PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource - GitHub Copilot Instructions

## Project Context

This is a PrismQ module for scraping YouTube Shorts content and storing idea inspirations in a SQLite database. It's part of the PrismQ Idea Sources ecosystem which includes:
- **PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource** - YouTube Shorts scraping (this module)
- **PrismQ.Idea.Sources.Content.Forums.RedditSource** - Reddit scraping (separate module)
- **StoryGenerator** - Automated story and video generation pipeline
- **PrismQ.RepositoryTemplate** - Standardized template for PrismQ modules
- Other specialized content source modules

## Target Platform

All code should be optimized for:
- **Operating System**: Windows (primary), Linux (development support)
- **GPU**: NVIDIA RTX 5090 (Ada Lovelace architecture, 32GB VRAM)
- **CPU**: AMD Ryzen processor (multi-core)
- **RAM**: 64GB DDR5
- **Python**: 3.10 or higher

## Development Guidelines

### Code Style
- Follow PEP 8 style guide for Python code
- Use type hints for all function parameters and return values
- Write comprehensive docstrings using Google style
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

Example function structure:
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

### Performance Considerations
- Optimize for GPU utilization on RTX 5090 (future AI features)
- Consider memory constraints (32GB VRAM, 64GB RAM)
- Use batch processing where applicable
- Implement proper resource management for API calls
- Profile performance-critical sections
- Implement proper CUDA memory management for AI workloads

### Testing
- Write unit tests for all new functionality
- Aim for >80% code coverage
- Include performance benchmarks for GPU-intensive operations
- Test on the target platform when possible
- Mock external API calls to avoid rate limits
- Use pytest fixtures for setup/teardown

Run tests:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_database.py::test_function_name
```

### Documentation
- Keep README.md up-to-date
- Document API changes
- Include usage examples
- Note platform-specific considerations
- Update docs/ for major features

## Common Tasks

### Adding New Features
1. Create issue in `issues/new/`
2. Move to `issues/wip/` when starting work
3. Write tests first (TDD approach)
4. Implement feature
5. Update documentation
6. Run full test suite
7. Move issue to `issues/done/`

### Extending YouTube Shorts Functionality
1. Enhance the YouTube plugin in `src/sources/youtube_plugin.py`
2. Update the `scrape()` method to add new capabilities
3. Add any new configuration options to `src/config.py`
4. Add factory method adjustments to `UniversalMetrics` if needed
5. Add tests in `tests/`
6. Update documentation in `docs/`

### Development Setup
```bash
# Clone and setup
git clone https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource.git
cd PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux

# Install dependencies
pip install -r requirements.txt

# Configure
copy .env.example .env  # Windows
# cp .env.example .env  # Linux
```

### Running the Application
```bash
# Scrape YouTube Shorts
python -m src.cli scrape

# List collected ideas
python -m src.cli list

# View statistics
python -m src.cli stats

# Clear database
python -m src.cli clear
```

### Common Debugging Tasks
```bash
# Check configuration
python -c "from src.config import Config; c = Config(); print(c.__dict__)"

# Test database connection
python -c "from src.database import Database; db = Database(':memory:'); print('OK')"

# Reset database
rm ideas.db
# or
python -m src.cli clear
```

## Code Organization

### Project Structure
```
PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource/
├── src/                    # Main source code
│   ├── cli.py              # CLI interface
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   ├── metrics.py          # Universal metrics system
│   ├── scoring/            # Scoring engine
│   └── sources/            # Source plugins
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── issues/                 # Issue tracking
```

### File Organization Guidelines
- Keep source plugins in `src/sources/`
- Add tests in `tests/` with `test_` prefix
- Update configuration in `src/config.py`
- CLI commands in `src/cli.py`

## Dependencies

- Prefer well-maintained, GPU-accelerated libraries for AI features
- Document version requirements clearly
- Consider CUDA/cuDNN compatibility
- Test compatibility with PyTorch/TensorFlow if using deep learning
- Ensure CUDA toolkit version compatibility

Update dependencies:
```bash
pip freeze > requirements.txt
# or manually edit requirements.txt with version constraints
```

## AI/ML Considerations

When working with AI models for future features:
- Use mixed precision (FP16/BF16) for RTX 5090
- Implement proper batch sizing for 32GB VRAM
- Use CUDA graphs for repetitive operations
- Profile GPU memory usage
- Consider model quantization for efficiency
- Implement proper CUDA memory management
- Test compatibility with PyTorch/TensorFlow frameworks
- Ensure CUDA/cuDNN version compatibility

## Integration with PrismQ Ecosystem

### Module Compatibility
- Follow consistent naming conventions across PrismQ modules
- Use compatible data formats for inter-module communication
- Document integration points with other PrismQ modules
- Consider pipeline compatibility with StoryGenerator and other modules

### Data Export
- Ensure collected ideas can be easily exported for downstream modules
- Maintain consistent schema for idea metadata (universal metrics)
- Support various output formats (JSON, CSV, database)

### Adding Support for Other Platforms
To add support for other platforms (TikTok, Instagram Reels, etc.), create a new repository following the PrismQ Idea Sources taxonomy:
- `PrismQ.Idea.Sources.Content.Shorts.TikTokSource`
- `PrismQ.Idea.Sources.Content.Shorts.InstagramReelsSource`

See the [PrismQ.RepositoryTemplate](https://github.com/Nomoos/PrismQ.RepositoryTemplate) for structure guidelines.

## Questions to Ask

Before implementing features, consider:
- Does this leverage the RTX 5090 efficiently (if AI-related)?
- Is this compatible with the PrismQ ecosystem?
- Have I included proper error handling?
- Are there edge cases to consider?
- Is the code documented and tested?
- Does this follow Python best practices?
- Is this optimized for Windows platform?

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

## Resources

- [Main README](../README.md)
- [Contributing Guidelines](../docs/CONTRIBUTING.md)
- [Metrics Documentation](../docs/METRICS.md)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
