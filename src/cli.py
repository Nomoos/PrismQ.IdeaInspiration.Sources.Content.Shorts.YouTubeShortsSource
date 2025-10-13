"""Command-line interface for PrismQ.Idea.Sources.Content.Shorts.YouTubeShortsSource."""

import click
import sys
from pathlib import Path
from src.config import Config
from src.database import Database
from src.metrics import UniversalMetrics
from src.sources.youtube_plugin import YouTubePlugin
from src.sources.youtube_channel_plugin import YouTubeChannelPlugin
from src.sources.youtube_trending_plugin import YouTubeTrendingPlugin


@click.group()
@click.version_option(version='1.0.0')
def main():
    """PrismQ YouTube Shorts Source - Gather idea inspirations from YouTube Shorts."""
    pass


@main.command()
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
def scrape(env_file):
    """Scrape ideas from YouTube Shorts (YouTube API - Legacy).
    
    ⚠️  NOT RECOMMENDED: Use scrape-channel, scrape-trending, or scrape-keyword instead.
    These yt-dlp methods provide richer metadata and no API quota limits.
    
    This command uses YouTube Data API v3 and is kept for backward compatibility.
    """
    try:
        # Warn user about better alternatives
        click.echo("⚠️  WARNING: You're using the legacy YouTube API scraper.", err=True)
        click.echo("   Consider using these yt-dlp-based alternatives instead:", err=True)
        click.echo("   - scrape-channel: Scrape from specific channels", err=True)
        click.echo("   - scrape-trending: Scrape from trending page", err=True)
        click.echo("   - scrape-keyword: Search by keywords", err=True)
        click.echo("   Benefits: No API limits, richer metadata, subtitles, story detection", err=True)
        click.echo("", err=True)
        # Load configuration
        config = Config(env_file)
        
        # Initialize database
        db = Database(config.database_path)
        
        # Initialize YouTube plugin
        try:
            youtube_plugin = YouTubePlugin(config)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        
        # Scrape from YouTube
        total_scraped = 0
        total_saved = 0
        
        click.echo("Scraping from YouTube Shorts...")
        
        try:
            ideas = youtube_plugin.scrape()
            total_scraped = len(ideas)
            click.echo(f"Found {len(ideas)} ideas from YouTube Shorts")
            
            # Process and save each idea
            for idea in ideas:
                # Convert platform metrics to universal metrics
                universal_metrics = UniversalMetrics.from_youtube(idea['metrics'])
                
                # Save to database with universal metrics
                success = db.insert_idea(
                    source='youtube',
                    source_id=idea['source_id'],
                    title=idea['title'],
                    description=idea['description'],
                    tags=idea['tags'],
                    score=universal_metrics.engagement_rate or 0.0,  # Use engagement rate as score
                    score_dictionary=universal_metrics.to_dict()
                )
                
                if success:
                    total_saved += 1
            
        except Exception as e:
            click.echo(f"Error scraping YouTube Shorts: {e}", err=True)
        
        click.echo(f"\nScraping complete!")
        click.echo(f"Total ideas found: {total_scraped}")
        click.echo(f"Total ideas saved: {total_saved}")
        click.echo(f"Database: {config.database_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command('scrape-channel')
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
@click.option('--channel', '-c', help='YouTube channel URL, handle (@username), or ID')
@click.option('--top', '-t', type=int, help='Number of shorts to scrape (default: config or 10)')
def scrape_channel(env_file, channel, top):
    """Scrape ideas from a specific YouTube channel's Shorts using yt-dlp.
    
    This command uses yt-dlp to scrape comprehensive metadata from a YouTube
    channel's Shorts, including subtitles, video quality metrics, and detailed
    engagement analytics.
    
    Examples:
        python -m src.cli scrape-channel --channel @channelname
        python -m src.cli scrape-channel --channel https://www.youtube.com/@channelname --top 20
        python -m src.cli scrape-channel --channel UC1234567890 --top 15
    """
    try:
        # Load configuration
        config = Config(env_file)
        
        # Initialize database
        db = Database(config.database_path)
        
        # Initialize YouTube channel plugin
        try:
            channel_plugin = YouTubeChannelPlugin(config)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("\nInstall yt-dlp with: pip install yt-dlp", err=True)
            sys.exit(1)
        
        # Scrape from YouTube channel
        total_scraped = 0
        total_saved = 0
        
        # Determine channel URL
        if channel:
            channel_url = channel
        elif config.youtube_channel_url:
            channel_url = config.youtube_channel_url
        else:
            click.echo("Error: No channel specified. Use --channel or set YOUTUBE_CHANNEL_URL in .env", err=True)
            sys.exit(1)
        
        # Determine number of shorts to scrape
        shorts_count = top if top else config.youtube_channel_max_shorts
        
        click.echo(f"Scraping from YouTube channel: {channel_url}")
        click.echo(f"Number of shorts to scrape: {shorts_count}")
        click.echo("")
        
        try:
            ideas = channel_plugin.scrape(channel_url=channel_url, top_n=shorts_count)
            total_scraped = len(ideas)
            click.echo(f"\nFound {len(ideas)} shorts from channel")
            
            # Process and save each idea
            for idea in ideas:
                # Convert platform metrics to universal metrics
                universal_metrics = UniversalMetrics.from_youtube(idea['metrics'])
                
                # Save to database with universal metrics
                success = db.insert_idea(
                    source='youtube_channel',
                    source_id=idea['source_id'],
                    title=idea['title'],
                    description=idea['description'],
                    tags=idea['tags'],
                    score=universal_metrics.engagement_rate or 0.0,
                    score_dictionary=universal_metrics.to_dict()
                )
                
                if success:
                    total_saved += 1
            
        except Exception as e:
            click.echo(f"Error scraping YouTube channel: {e}", err=True)
            import traceback
            traceback.print_exc()
        
        click.echo(f"\nScraping complete!")
        click.echo(f"Total shorts found: {total_scraped}")
        click.echo(f"Total shorts saved: {total_saved}")
        click.echo(f"Database: {config.database_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@main.command('scrape-trending')
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
@click.option('--top', '-t', type=int, help='Number of shorts to scrape (default: config or 10)')
def scrape_trending(env_file, top):
    """Scrape ideas from YouTube trending Shorts using yt-dlp.
    
    This command scrapes Shorts from the YouTube trending page without requiring
    an API key. Uses yt-dlp for comprehensive metadata extraction.
    
    Examples:
        python -m src.cli scrape-trending
        python -m src.cli scrape-trending --top 15
    """
    try:
        # Load configuration
        config = Config(env_file)
        
        # Initialize database
        db = Database(config.database_path)
        
        # Initialize YouTube trending plugin
        try:
            trending_plugin = YouTubeTrendingPlugin(config)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("\nInstall yt-dlp with: pip install yt-dlp", err=True)
            sys.exit(1)
        
        # Scrape from trending
        total_scraped = 0
        total_saved = 0
        
        # Determine number of shorts to scrape
        shorts_count = top if top else getattr(config, 'youtube_trending_max_shorts', 10)
        
        click.echo(f"Scraping from YouTube trending")
        click.echo(f"Number of shorts to scrape: {shorts_count}")
        click.echo("")
        
        try:
            ideas = trending_plugin.scrape_trending(top_n=shorts_count)
            total_scraped = len(ideas)
            click.echo(f"\nFound {len(ideas)} shorts from trending")
            
            # Process and save each idea
            for idea in ideas:
                # Convert platform metrics to universal metrics
                universal_metrics = UniversalMetrics.from_youtube(idea['metrics'])
                
                # Save to database with universal metrics
                success = db.insert_idea(
                    source='youtube_trending',
                    source_id=idea['source_id'],
                    title=idea['title'],
                    description=idea['description'],
                    tags=idea['tags'],
                    score=universal_metrics.engagement_rate or 0.0,
                    score_dictionary=universal_metrics.to_dict()
                )
                
                if success:
                    total_saved += 1
            
        except Exception as e:
            click.echo(f"Error scraping YouTube trending: {e}", err=True)
            import traceback
            traceback.print_exc()
        
        click.echo(f"\nScraping complete!")
        click.echo(f"Total shorts found: {total_scraped}")
        click.echo(f"Total shorts saved: {total_saved}")
        click.echo(f"Database: {config.database_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@main.command('scrape-keyword')
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
@click.option('--keyword', '-k', required=True, help='Search keyword')
@click.option('--top', '-t', type=int, help='Number of shorts to scrape (default: config or 10)')
def scrape_keyword(env_file, keyword, top):
    """Scrape ideas from YouTube by keyword search using yt-dlp.
    
    This command searches for Shorts using keywords without requiring an API key.
    Uses yt-dlp for comprehensive metadata extraction.
    
    Examples:
        python -m src.cli scrape-keyword --keyword "startup ideas"
        python -m src.cli scrape-keyword --keyword "business tips" --top 20
    """
    try:
        # Load configuration
        config = Config(env_file)
        
        # Initialize database
        db = Database(config.database_path)
        
        # Initialize YouTube trending plugin (handles both trending and keyword)
        try:
            trending_plugin = YouTubeTrendingPlugin(config)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("\nInstall yt-dlp with: pip install yt-dlp", err=True)
            sys.exit(1)
        
        # Scrape from keyword
        total_scraped = 0
        total_saved = 0
        
        # Determine number of shorts to scrape
        shorts_count = top if top else getattr(config, 'youtube_keyword_max_shorts', 10)
        
        click.echo(f"Scraping from YouTube with keyword: '{keyword}'")
        click.echo(f"Number of shorts to scrape: {shorts_count}")
        click.echo("")
        
        try:
            ideas = trending_plugin.scrape_by_keyword(keyword, top_n=shorts_count)
            total_scraped = len(ideas)
            click.echo(f"\nFound {len(ideas)} shorts for keyword: '{keyword}'")
            
            # Process and save each idea
            for idea in ideas:
                # Convert platform metrics to universal metrics
                universal_metrics = UniversalMetrics.from_youtube(idea['metrics'])
                
                # Save to database with universal metrics
                success = db.insert_idea(
                    source='youtube_keyword',
                    source_id=idea['source_id'],
                    title=idea['title'],
                    description=idea['description'],
                    tags=idea['tags'],
                    score=universal_metrics.engagement_rate or 0.0,
                    score_dictionary=universal_metrics.to_dict()
                )
                
                if success:
                    total_saved += 1
            
        except Exception as e:
            click.echo(f"Error scraping YouTube keyword: {e}", err=True)
            import traceback
            traceback.print_exc()
        
        click.echo(f"\nScraping complete!")
        click.echo(f"Total shorts found: {total_scraped}")
        click.echo(f"Total shorts saved: {total_saved}")
        click.echo(f"Database: {config.database_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)



@main.command()
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
@click.option('--limit', '-l', type=int, default=20, 
              help='Maximum number of ideas to display')
@click.option('--source', '-s', help='Filter by source')
def list(env_file, limit, source):
    """List collected ideas."""
    try:
        # Load configuration
        config = Config(env_file)
        
        # Open database
        db = Database(config.database_path)
        
        # Get ideas
        ideas = db.get_all_ideas(limit=limit)
        
        # Filter by source if specified
        if source:
            ideas = [idea for idea in ideas if idea['source'] == source]
        
        if not ideas:
            click.echo("No ideas found.")
            return
        
        # Display ideas
        click.echo(f"\n{'='*80}")
        click.echo(f"Collected Ideas ({len(ideas)} total)")
        click.echo(f"{'='*80}\n")
        
        for i, idea in enumerate(ideas, 1):
            click.echo(f"{i}. [{idea['source'].upper()}] {idea['title']}")
            click.echo(f"   ID: {idea['source_id']}")
            if idea['tags']:
                click.echo(f"   Tags: {idea['tags']}")
            if idea['description']:
                desc = idea['description'][:150]
                if len(idea['description']) > 150:
                    desc += "..."
                click.echo(f"   Description: {desc}")
            click.echo()
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
def stats(env_file):
    """Show statistics about collected ideas."""
    try:
        # Load configuration
        config = Config(env_file)
        
        # Open database
        db = Database(config.database_path)
        
        # Get all ideas
        ideas = db.get_all_ideas()
        
        if not ideas:
            click.echo("No ideas collected yet.")
            return
        
        # Calculate statistics
        total = len(ideas)
        by_source = {}
        
        for idea in ideas:
            source = idea['source']
            by_source[source] = by_source.get(source, 0) + 1
        
        # Display statistics
        click.echo(f"\n{'='*50}")
        click.echo(f"Idea Collection Statistics")
        click.echo(f"{'='*50}\n")
        click.echo(f"Total Ideas: {total}\n")
        click.echo(f"Ideas by Source:")
        for source, count in sorted(by_source.items()):
            percentage = (count / total) * 100
            click.echo(f"  {source.capitalize()}: {count} ({percentage:.1f}%)")
        click.echo()
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
@click.confirmation_option(prompt='Are you sure you want to clear all ideas?')
def clear(env_file):
    """Clear all ideas from the database."""
    try:
        # Load configuration
        config = Config(env_file)
        
        # Delete database file
        db_path = Path(config.database_path)
        if db_path.exists():
            db_path.unlink()
            click.echo(f"Database cleared: {config.database_path}")
        else:
            click.echo("Database does not exist.")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
