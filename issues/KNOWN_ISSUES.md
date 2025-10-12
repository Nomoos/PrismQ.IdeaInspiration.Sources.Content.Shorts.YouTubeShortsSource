# Known Issues

This document tracks known issues and their workarounds.

## Common Issues

### Windows-Specific Issues

#### Module Not Found Error
**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: 
- Ensure you're running commands from the project root directory
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

#### Path Issues
**Problem**: Path errors when accessing files

**Solution**:
- Use forward slashes (/) or escaped backslashes (\\\\) in paths
- Check that `.env` file uses correct path format for Windows

#### API Errors
**Problem**: API authentication failures

**Solution**:
- Verify API credentials in `.env` file are correct
- Ensure no extra spaces or quotes around values
- Check API keys are active in respective platforms

### General Issues

#### No Ideas Scraped
**Problem**: Commands complete but no ideas are collected

**Solution**:
- Verify YouTube API credentials are correct
- Check internet connection
- Ensure YouTube API service is accessible
- Check API quotas haven't been exceeded

#### Database Locked Error
**Problem**: `database is locked` error

**Solution**:
- Close any other processes accessing the database file
- Ensure only one instance of the application is running
- Delete lock files if present

#### Rate Limiting
**Problem**: YouTube API rate limit errors

**Solution**:
- Reduce `YOUTUBE_MAX_RESULTS` value in `.env`
- Add delays between requests
- YouTube API: 10,000 units/day quota
- Consider spreading requests across multiple days

### Installation Issues

#### Python Version Compatibility
**Problem**: Syntax or compatibility errors

**Solution**:
- Ensure Python 3.8 or higher is installed
- Check version with `python --version`
- Use `python3` instead of `python` on some systems

#### Dependency Installation Failures
**Problem**: Failed to install requirements

**Solution**:
- Upgrade pip: `pip install --upgrade pip`
- Install dependencies individually if batch fails
- Use virtual environment to avoid conflicts

## Reporting New Issues

If you encounter an issue not listed here:

1. Check [GitHub Issues](https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource/issues)
2. Open a new issue with detailed information
3. Include error logs, environment details, and reproduction steps

## Getting Help

- **Documentation**: See [README.md](../README.md)
- **Contributing Guide**: See [CONTRIBUTING.md](../docs/CONTRIBUTING.md)
- **Discussions**: Use [GitHub Discussions](https://github.com/Nomoos/PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource/discussions)
