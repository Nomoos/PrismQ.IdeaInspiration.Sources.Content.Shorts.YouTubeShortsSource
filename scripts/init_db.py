"""Database initialization script for PrismQ YouTube Shorts Source.

This script initializes the database schema and ensures all tables are created.
Similar to PrismQ.IdeaInspiration.Model initialization approach.
"""

import sys
from pathlib import Path

# Add parent directory to path to allow importing Model
sys.path.insert(0, str(Path(__file__).parent.parent))

from Model import DBContext


def init_db(db_path: str = "ideas.db", verbose: bool = True):
    """Initialize the database schema.
    
    Args:
        db_path: Path to SQLite database file
        verbose: Print status messages
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if verbose:
            print(f"Initializing database at: {db_path}")
        
        # Ensure parent directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create database context (this will create tables)
        with DBContext(db_path) as db_context:
            if verbose:
                print("Database schema created successfully!")
                print(f"Tables created:")
                print("  - youtube_video")
                
                # Show statistics
                count = db_context.count()
                print(f"\nCurrent record count: {count}")
        
        return True
        
    except Exception as e:
        if verbose:
            print(f"Error initializing database: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialize PrismQ YouTube Shorts Source database"
    )
    parser.add_argument(
        '--db-path',
        default='ideas.db',
        help='Path to SQLite database file (default: ideas.db)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output messages'
    )
    
    args = parser.parse_args()
    
    success = init_db(db_path=args.db_path, verbose=not args.quiet)
    
    if success:
        if not args.quiet:
            print("\n✓ Database initialization completed successfully!")
        sys.exit(0)
    else:
        if not args.quiet:
            print("\n✗ Database initialization failed!", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
