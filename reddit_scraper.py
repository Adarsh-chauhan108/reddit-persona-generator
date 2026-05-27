"""
Reddit Scraper Module
Handles authentication and data extraction from Reddit using PRAW.
"""


import os
import logging
import praw
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class RedditScraper:
    """Scrapes Reddit posts and comments for a given user."""
    
    def __init__(self):
        """Initialize Reddit API client."""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'PersonaGenerator/1.0')
        )
        
        # Verify authentication
        try:
            self.reddit.user.me()
            logger.info("Successfully authenticated with Reddit API")
        except Exception as e:
            logger.warning(f"Reddit API authentication failed: {e}")
    
    def scrape_user_data(self, username: str, limit: int = 100) -> List[Dict]:
        """
        Scrape posts and comments from a Reddit user.
        
        Args:
            username: Reddit username (without u/ prefix)
            limit: Maximum number of items to fetch
            
        Returns:
            List of dictionaries containing post/comment data
        """
        user_data = []
        
        try:
            user = self.reddit.redditor(username)
            
            # Check if user exists
            try:
                user.id
            except Exception:
                logger.error(f"User u/{username} not found or suspended")
                return []
            
            logger.info(f"Fetching data for user: u/{username}")
            
            # Fetch submissions (posts)
            submissions_count = 0
            try:
                for submission in user.submissions.new(limit=limit//2):
                    if submissions_count >= limit//2:
                        break
                    
                    # Skip deleted/removed posts
                    if submission.selftext == '[deleted]' or submission.selftext == '[removed]':
                        continue
                    
                    post_data = {
                        'type': 'post',
                        'content': f"Title: {submission.title}\n\nBody: {submission.selftext}",
                        'subreddit': submission.subreddit.display_name,
                        'permalink': f"https://reddit.com{submission.permalink}",
                        'created_utc': submission.created_utc,
                        'score': submission.score,
                        'url': submission.url if submission.url != submission.permalink else None
                    }
                    
                    user_data.append(post_data)
                    submissions_count += 1
                    
            except Exception as e:
                logger.warning(f"Error fetching submissions: {e}")
            
            # Fetch comments
            comments_count = 0
            try:
                for comment in user.comments.new(limit=limit//2):
                    if comments_count >= limit//2:
                        break
                    
                    # Skip deleted/removed comments
                    if comment.body in ['[deleted]', '[removed]']:
                        continue
                    
                    comment_data = {
                        'type': 'comment',
                        'content': comment.body,
                        'subreddit': comment.subreddit.display_name,
                        'permalink': f"https://reddit.com{comment.permalink}",
                        'created_utc': comment.created_utc,
                        'score': comment.score,
                        'parent_id': comment.parent_id
                    }
                    
                    user_data.append(comment_data)
                    comments_count += 1
                    
            except Exception as e:
                logger.warning(f"Error fetching comments: {e}")
            
            logger.info(f"Fetched {submissions_count} posts and {comments_count} comments")
            
        except Exception as e:
            logger.error(f"Error scraping user data: {e}")
            return []
        
        # Sort by creation time (newest first)
        user_data.sort(key=lambda x: x['created_utc'], reverse=True)
        
        return user_data
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """
        Get basic user information.
        
        Args:
            username: Reddit username
            
        Returns:
            Dictionary with user info or None if not found
        """
        try:
            user = self.reddit.redditor(username)
            
            return {
                'username': user.name,
                'created_utc': user.created_utc,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'is_verified': user.verified,
                'is_premium': user.is_gold,
                'account_age_days': (datetime.now().timestamp() - user.created_utc) / 86400
            }
            
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
