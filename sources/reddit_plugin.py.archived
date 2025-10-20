"""Reddit source plugin for scraping idea inspirations."""

from typing import List, Dict, Any
import praw
from src.sources import SourcePlugin


class RedditPlugin(SourcePlugin):
    """Plugin for scraping ideas from Reddit."""

    def __init__(self, config):
        """Initialize Reddit plugin.
        
        Args:
            config: Configuration object
        """
        super().__init__(config)
        
        # Initialize Reddit API client
        if not config.reddit_client_id or not config.reddit_client_secret:
            raise ValueError("Reddit API credentials not configured")
        
        self.reddit = praw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent
        )

    def get_source_name(self) -> str:
        """Get the name of this source.
        
        Returns:
            Source name
        """
        return "reddit"

    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape ideas from configured subreddits.
        
        Returns:
            List of idea dictionaries
        """
        ideas = []
        
        for subreddit_name in self.config.reddit_subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get hot posts from the subreddit
                for post in subreddit.hot(limit=self.config.reddit_limit):
                    if post.stickied:  # Skip pinned posts
                        continue
                    
                    idea = {
                        'source_id': post.id,
                        'title': post.title,
                        'description': post.selftext if post.selftext else post.url,
                        'tags': self._extract_tags(post, subreddit_name),
                        'metrics': post  # Pass the full post object for UniversalMetrics
                    }
                    ideas.append(idea)
                    
            except Exception as e:
                print(f"Error scraping r/{subreddit_name}: {e}")
                continue
        
        return ideas

    def _extract_tags(self, post, subreddit_name: str) -> str:
        """Extract tags from a Reddit post.
        
        Args:
            post: Reddit post object
            subreddit_name: Name of the subreddit
            
        Returns:
            Comma-separated tag string
        """
        tags = [subreddit_name]
        
        # Add post flair if available
        if post.link_flair_text:
            tags.append(post.link_flair_text)
        
        # Add 'discussion' tag if it's a text post
        if post.is_self:
            tags.append('discussion')
        
        return self.format_tags(tags)
