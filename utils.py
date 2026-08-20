"""
Utility Functions
Helper functions for logging, validation, and other common tasks.
"""

import logging
import re
import sys
from typing import Optional

def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Suppress verbose logs from external libraries
    if not verbose:
        logging.getLogger('praw').setLevel(logging.WARNING)
        logging.getLogger('prawcore').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

def validate_username(username: str) -> bool:
    """
    Validate Reddit username format.
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not username:
        return False
    
    # Remove u/ prefix if present
    if username.startswith('u/'):
        username = username[2:]
    
    # Reddit username rules
    # - 3-20 characters
    # - Letters, numbers, underscore, hyphen
    # - Cannot start/end with underscore
    # - Cannot have consecutive underscores
    
    if len(username) < 3 or len(username) > 20:
        return False
    
    if not re.match(r'^[A-Za-z0-9_-]+$', username):
        return False
    
    if username.startswith('_') or username.endswith('_'):
        return False
    
    if '__' in username:
        return False
    
    return True

def clean_username(username: str) -> str:
    """
    Clean and normalize username.
    
    Args:
        username: Raw username input
        
    Returns:
        Cleaned username
    """
    if not username:
        return ''
    
    # Remove u/ prefix if present
    if username.startswith('u/'):
        username = username[2:]
    
    # Remove /user/ prefix if present
    if username.startswith('/user/'):
        username = username[6:]
    
    # Remove any trailing slashes
    username = username.rstrip('/')
    
    return username.strip()

def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to readable string.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted date string
    """
    from datetime import datetime
    
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, OSError):
        return 'Unknown'

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + '...'

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def get_subreddit_categories() -> dict:
    """
    Get common subreddit categories for analysis.
    
    Returns:
        Dictionary mapping subreddit names to categories
    """
    return {
        # Technology
        'programming': 'Technology',
        'python': 'Technology',
        'javascript': 'Technology',
        'webdev': 'Technology',
        'technology': 'Technology',
        'MachineLearning': 'Technology',
        'artificial': 'Technology',
        'datascience': 'Technology',
        
        # Gaming
        'gaming': 'Gaming',
        'Steam': 'Gaming',
        'PS4': 'Gaming',
        'PS5': 'Gaming',
        'xbox': 'Gaming',
        'NintendoSwitch': 'Gaming',
        'pcgaming': 'Gaming',
        
        # Finance
        'personalfinance': 'Finance',
        'investing': 'Finance',
        'stocks': 'Finance',
        'cryptocurrency': 'Finance',
        'Bitcoin': 'Finance',
        
        # Health & Fitness
        'fitness': 'Health & Fitness',
        'loseit': 'Health & Fitness',
        'nutrition': 'Health & Fitness',
        'mentalhealth': 'Health & Fitness',
        
        # Entertainment
        'movies': 'Entertainment',
        'television': 'Entertainment',
        'music': 'Entertainment',
        'books': 'Entertainment',
        'Marvel': 'Entertainment',
        
        # Education
        'AskReddit': 'General Discussion',
        'explainlikeimfive': 'Education',
        'todayilearned': 'Education',
        'science': 'Education',
        
        # Lifestyle
        'food': 'Lifestyle',
        'cooking': 'Lifestyle',
        'DIY': 'Lifestyle',
        'gardening': 'Lifestyle',
        'travel': 'Lifestyle',
        
        # News & Politics
        'news': 'News & Politics',
        'politics': 'News & Politics',
        'worldnews': 'News & Politics',
        
        # Sports
        'sports': 'Sports',
        'nba': 'Sports',
        'nfl': 'Sports',
        'soccer': 'Sports',
        'baseball': 'Sports',
    }

def categorize_subreddit(subreddit_name: str) -> str:
    """
    Categorize a subreddit based on its name.
    
    Args:
        subreddit_name: Name of the subreddit
        
    Returns:
        Category name or 'Other' if unknown
    """
    categories = get_subreddit_categories()
    return categories.get(subreddit_name, 'Other')
