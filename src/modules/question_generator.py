import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from typing import Dict, Tuple
import asyncio
from datetime import datetime

import streamlit as st


class QuestionGenerator():
    """Use Azure AI to generate questions from a given category chosen by the user"""

    def __init__(self):
        load_dotenv()

        # Load Azure OpenAI credentials
        self.api_key = st.secrets['AZURE_API_KEY']
        self.endpoint = st.secrets['MODEL_URI']

        self.last_request_time = None
        self.min_request_interval = 1.0  # Minimum interval between requests in seconds

        if not self.api_key or not self.endpoint:
            raise ValueError(
                "Azure OpenAI credentials not found in environment")

        # Configure OpenAI client
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version='2024-08-01-preview'
        )

    async def generate_question(self, context: Dict) -> Tuple[bool, str]:
        """Generate a contextually appropriate IELTS question"""
        try:
            # Rate limiting check
            now = datetime.now()
            if self.last_request_time:
                time_since_last = (now - self.last_request_time).total_seconds()
                if time_since_last < self.min_request_interval:
                    await asyncio.sleep(self.min_request_interval - time_since_last)
            
            # Update last request time
            self.last_request_time = now

            # Extract context information
            topic = context.get('topic', '')
            difficulty = context.get('difficulty', 1.0)
            history = context.get('history', [])

            # Create system prompt
            system_prompt = """You are an IELTS Speaking examiner. Generate appropriate questions 
            based on the topic and conversation history. Questions should:
            - Be clear and natural
            - Match IELTS speaking test style
            - Progress logically from previous questions
            - Adapt to the specified difficulty level (0-2)"""

            # Create conversation prompt
            user_prompt = f"""Topic: {topic}
            Difficulty: {difficulty}
            Previous exchanges: {history if history else 'None'}
            Generate a natural follow-up question."""

            # Call Azure OpenAI API
            response = self.client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )

            # Extract generated question
            question = response.choices[0].message.content.strip()

            return True, question

        except Exception as e:
            return False, f"Error generating question: {str(e)}"

    def _adjust_difficulty(self, current_difficulty: float, user_performance: float) -> float:
        """Adjust question difficulty based on user performance"""
        # Performance is expected to be between 0-9 (IELTS scale)
        performance_normalized = user_performance / 9.0

        # Calculate difficulty adjustment
        adjustment = 0.1 * (performance_normalized - 0.5)
        new_difficulty = current_difficulty + adjustment

        # Clamp difficulty between 0-2
        return max(0.0, min(2.0, new_difficulty))
