#!/usr/bin/env python3
"""
Reddit Persona Generator - Main Entry Point
Analyzes a Reddit user's posts and comments to generate a detailed persona.
"""
import argparse
import os
import sys
from dotenv import load_dotenv

from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator
from utils import setup_logging, validate_username

# Load environment variables
load_dotenv()

def main():
    """Main function to run the Reddit persona generator."""
    parser = argparse.ArgumentParser(
        description="Generate a detailed persona from Reddit user's posts and comments"
    )
    parser.add_argument(
        "username",
        help="Reddit username to analyze (without u/ prefix)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of posts/comments to analyze (default: 100)"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save the persona file (default: output)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Validate username
    if not validate_username(args.username):
        print(f"Error: Invalid username '{args.username}'")
        sys.exit(1)
    
    # Check for required environment variables
    required_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        sys.exit(1)
    
    try:
        # Initialize scraper and generator
        scraper = RedditScraper()
        generator = PersonaGenerator()
        
        print(f"📊 Analyzing user: u/{args.username}")
        print(f"🔍 Fetching up to {args.limit} posts/comments...")
        
        # Scrape Reddit data
        user_data = scraper.scrape_user_data(args.username, limit=args.limit)
        
        if not user_data:
            print(f"❌ No data found for user u/{args.username}")
            sys.exit(1)
        
        print(f"✅ Found {len(user_data)} posts/comments")
        print("🤖 Generating persona with AI...")
        
        # Generate persona
        persona = generator.generate_persona(user_data)
        
        # Save to file
        output_path = os.path.join(args.output_dir, f"{args.username}_persona.txt")
        os.makedirs(args.output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(persona)
        
        print(f"✅ Persona saved to: {output_path}")
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
