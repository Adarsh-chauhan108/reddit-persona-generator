"""
Persona Generator Module
Uses OpenAI API to analyze Reddit data and generate user personas.
"""

import os
import logging
import openai
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class PersonaGenerator:
    """Generates user personas using OpenAI API."""
    
    def __init__(self):
        """Initialize OpenAI API client."""
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
    def generate_persona(self, user_data: List[Dict]) -> str:
        """
        Generate a detailed persona from user's Reddit data.
        
        Args:
            user_data: List of posts/comments data
            
        Returns:
            Formatted persona text with citations
        """
        if not user_data:
            return "No data available to generate persona."
        
        
        content_summary = self._prepare_content_summary(user_data)
        
        # Create the prompt
        prompt = self._create_persona_prompt(content_summary)
        
        try:
            logger.info("Generating persona with OpenAI API...")
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in personality analysis and user profiling. Analyze the provided Reddit data to create a comprehensive user persona. Be objective, evidence-based, and cite specific examples."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            persona_text = response.choices[0].message.content
            
            # Add header and formatting
            formatted_persona = self._format_persona(persona_text, user_data)
            
            logger.info("Persona generated successfully")
            return formatted_persona
            
        except Exception as e:
            logger.error(f"Error generating persona: {e}")
            return f"Error generating persona: {str(e)}"
    
    def _prepare_content_summary(self, user_data: List[Dict]) -> str:
        """
        Prepare a summary of user's content for analysis.
        
        Args:
            user_data: List of posts/comments data
            
        Returns:
            Formatted content summary
        """
        summary_parts = []
        
        # Group by subreddit for better analysis
        subreddit_activity = {}
        for item in user_data:
            subreddit = item['subreddit']
            if subreddit not in subreddit_activity:
                subreddit_activity[subreddit] = []
            subreddit_activity[subreddit].append(item)
        
        # Add subreddit activity overview
        summary_parts.append("=== SUBREDDIT ACTIVITY ===")
        for subreddit, items in sorted(subreddit_activity.items(), key=lambda x: len(x[1]), reverse=True):
            summary_parts.append(f"r/{subreddit}: {len(items)} posts/comments")
        
        summary_parts.append("\n=== CONTENT SAMPLES ===")
        
        # Add content samples (limit to prevent token overflow)
        for i, item in enumerate(user_data[:50]):  # Limit to 50 items
            content_preview = item['content'][:500]  # Limit content length
            if len(item['content']) > 500:
                content_preview += "..."
            
            summary_parts.append(
                f"\n[{i+1}] {item['type'].upper()} in r/{item['subreddit']}"
                f"\nContent: {content_preview}"
                f"\nScore: {item['score']}"
                f"\nPermalink: {item['permalink']}"
                f"\n---"
            )
        
        return "\n".join(summary_parts)
    
    def _create_persona_prompt(self, content_summary: str) -> str:
        """
        Create the analysis prompt for OpenAI.
        
        Args:
            content_summary: Prepared content summary
            
        Returns:
            Formatted prompt
        """
        prompt = f"""
Analyze the following Reddit user data and generate a comprehensive persona. For each insight, provide specific citations from the data.

{content_summary}

Please generate a detailed persona covering these aspects:

## 📍 Location
Analyze any geographical references or location indicators.

## 💼 Profession/Field of Interest
Identify their career, job, or main professional interests.

## 🎓 Education Level
Assess their educational background or intellectual level.

## 🎮 Hobbies and Interests
List their main hobbies, interests, and activities.

## 🧠 Personality Traits
Analyze their communication style, behavior patterns, and personality.

## 🗣 Communication Style
Describe how they communicate and interact with others.

## 🤖 Tech Savviness
Assess their technical knowledge and digital literacy.

## 🎯 Values and Beliefs
Identify their core values, beliefs, or ideological leanings.

## 📊 Activity Patterns
Analyze their Reddit usage patterns and preferred communities.

For each section, provide:
1. Your analysis/conclusion
2. Supporting evidence with specific citations (permalink references)
3. Confidence level (High/Medium/Low)

Be objective, evidence-based, and avoid speculation without supporting data.
"""
        
        return prompt
    
    def _format_persona(self, persona_text: str, user_data: List[Dict]) -> str:
        """
        Format the final persona output.
        
        Args:
            persona_text: Generated persona text
            user_data: Original user data
            
        Returns:
            Formatted persona with header and metadata
        """
        header = f"""
# Reddit User Persona Analysis
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Data Points Analyzed:** {len(user_data)}
**Analysis Model:** {self.model}

---

"""
        
        footer = f"""

---

## Data Summary
- **Total Posts:** {len([item for item in user_data if item['type'] == 'post'])}
- **Total Comments:** {len([item for item in user_data if item['type'] == 'comment'])}
- **Subreddits Active In:** {len(set(item['subreddit'] for item in user_data))}
- **Date Range:** {datetime.fromtimestamp(min(item['created_utc'] for item in user_data)).strftime('%Y-%m-%d')} to {datetime.fromtimestamp(max(item['created_utc'] for item in user_data)).strftime('%Y-%m-%d')}

## Disclaimer
This persona is generated based on publicly available Reddit data and AI analysis. It should be used for research and educational purposes only. The analysis may not reflect the complete personality or current views of the user.
"""
        
        return header + persona_text + footer
