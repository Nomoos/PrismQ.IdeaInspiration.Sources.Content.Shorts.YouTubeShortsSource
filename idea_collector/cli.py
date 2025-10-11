"""Command-line interface for PrismQ.IdeaCollector."""

import click
import sys
from pathlib import Path
from idea_collector.config import Config
from idea_collector.database import Database
from idea_collector.sources.reddit_plugin import RedditPlugin
from idea_collector.sources.youtube_plugin import YouTubePlugin


@click.group()
@click.version_option(version='1.0.0')
def main():
    """PrismQ.IdeaCollector - Gather idea inspirations from multiple sources."""
    pass


@main.command()
@click.option('--source', '-s', type=click.Choice(['reddit', 'youtube', 'all']), 
              default='all', help='Source to scrape ideas from')
@click.option('--env-file', '-e', type=click.Path(exists=True), 
              help='Path to .env file')
def scrape(source, env_file):
    """Scrape ideas from configured sources."""
    try:
        # Load configuration
        config = Config(env_file)
        
        # Initialize database
        db = Database(config.database_path)
        
        # Determine which sources to scrape
        sources_to_scrape = []
        if source == 'all' or source == 'reddit':
            try:
                sources_to_scrape.append(RedditPlugin(config))
            except ValueError as e:
                click.echo(f"Warning: Skipping Reddit - {e}", err=True)
        
        if source == 'all' or source == 'youtube':
            try:
                sources_to_scrape.append(YouTubePlugin(config))
            except ValueError as e:
                click.echo(f"Warning: Skipping YouTube - {e}", err=True)
        
        if not sources_to_scrape:
            click.echo("Error: No valid sources configured. Check your .env file.", err=True)
            sys.exit(1)
        
        # Scrape from each source
        total_scraped = 0
        total_saved = 0
        
        for plugin in sources_to_scrape:
            source_name = plugin.get_source_name()
            click.echo(f"Scraping from {source_name}...")
            
            try:
                ideas = plugin.scrape()
                total_scraped += len(ideas)
                click.echo(f"Found {len(ideas)} ideas from {source_name}")
                
                # Process and save each idea
                for idea in ideas:
                    # Save to database with a simple placeholder score
                    success = db.insert_idea(
                        source=source_name,
                        source_id=idea['source_id'],
                        title=idea['title'],
                        description=idea['description'],
                        tags=idea['tags'],
                        score=1.0,  # Placeholder score
                        score_dictionary={}  # Empty dictionary
                    )
                    
                    if success:
                        total_saved += 1
                
            except Exception as e:
                click.echo(f"Error scraping {source_name}: {e}", err=True)
        
        click.echo(f"\nScraping complete!")
        click.echo(f"Total ideas found: {total_scraped}")
        click.echo(f"Total ideas saved: {total_saved}")
        click.echo(f"Database: {config.database_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
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
