# src/modules/scoring.py
from typing import Dict, List
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import time
import datetime
import asyncio


class ScoringEngine:
    """IELTS scoring engine that evaluates responses across multiple criteria"""

    def __init__(self):
        load_dotenv()
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key='DaONNemP3XA2BKtvLbGFj1JzgeU1l3Ds0bhuAQgvoQ4XMNqI8RqmJQQJ99BCACHYHv6XJ3w3AAAAACOGD0gz',
            azure_endpoint='https://kdube-m8h69gib-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview',
            api_version='2024-12-01-preview'
        )

        self.requests_per_minute = 60
        self.last_request_time = {}
        self.min_request_interval = 1.0

        self.rate_limiter = RequestRateLimiter(self.requests_per_minute)


        # Define weights for each scoring criterion
        self.criteria_weights = {
            'fluency': 0.25,
            'lexical': 0.25,
            'grammar': 0.25,
            'pronunciation': 0.25
        }

        # Map full category names to short names
        self.category_mapping = {
            'Fluency & Coherence': 'fluency',
            'Lexical Resource': 'lexical',
            'Grammatical Range & Accuracy': 'grammar',
            'Pronunciation': 'pronunciation'
        }

    async def evaluate_response(self, response: str, audio_duration: float) -> Dict:
        """Evaluate a response across all IELTS criteria"""
        try:
            await self.rate_limiter.wait_if_needed()

            # Create prompt for scoring the response
            scoring_prompt = f"""
            Analyze the following IELTS speaking response:
            "{response}"
            Duration: {audio_duration} seconds

            Rate each criterion (0-9) and provide brief feedback.
            Format each line exactly as: Category|Score|Feedback

            Categories to evaluate:
            - Fluency & Coherence
            - Lexical Resource
            - Grammatical Range & Accuracy
            - Pronunciation
            """

            print("DEBUG: Sending evaluation request...")

            # Send request to Azure OpenAI for evaluation
            analysis = self.client.chat.completions.create(
                model='gpt-4',  # Ensure this matches your Azure deployment
                messages=[
                    {"role": "system", "content": "You are an IELTS examiner. Provide clear, structured evaluations."},
                    {"role": "user", "content": scoring_prompt}
                ],
                temperature=0.3,
            )

            content = analysis.choices[0].message.content
            print(f"DEBUG: Raw API response: {content[:100]}...")

            scores = {}
            feedback = {}

            # Parse the response content
            for line in content.split('\n'):
                if '|' not in line:
                    continue

                parts = line.split('|')
                if len(parts) != 3:
                    continue

                category, score_str, explanation = parts
                category = category.strip()

                if category not in self.category_mapping:
                    continue

                normalized_category = self.category_mapping[category]
                try:
                    score = float(score_str.strip())
                    score = max(0.0, min(9.0, score))  # Clamp between 0-9
                except ValueError:
                    score = 5.0  # Default score

                scores[normalized_category] = score
                feedback[normalized_category] = {
                    'score': score,
                    'suggestions': [explanation.strip()],
                    'examples': []
                }

            # Ensure all categories are present
            for full_name, short_name in self.category_mapping.items():
                if short_name not in scores:
                    scores[short_name] = 5.0
                    feedback[short_name] = {
                        'score': 5.0,
                        'suggestions': [f"Unable to evaluate {full_name}"],
                        'examples': []
                    }

            overall_score = self._calculate_overall_score(scores)

            print(f"DEBUG: Evaluation complete. Scores: {scores}")

            return {
                'scores': scores,
                'feedback': feedback,
                'overall_score': overall_score
            }

        except Exception as e:
            print(f"ERROR in evaluation: {str(e)}")
            return self._get_default_evaluation()

    def _get_default_evaluation(self) -> Dict:
        """Return default evaluation when scoring fails"""
        default_scores = {
            category: 5.0 for category in self.category_mapping.values()}
        default_feedback = {
            category: {
                'score': 5.0,
                'suggestions': ['Evaluation unavailable'],
                'examples': []
            } for category in self.category_mapping.values()
        }

        return {
            'scores': default_scores,
            'feedback': default_feedback,
            'overall_score': 5.0
        }

    def _score_fluency(self, response: str, audio_duration: float) -> float:
        """Score fluency based on speech rate, pauses, and coherence"""
        # Calculate words per minute
        words = len(response.split())
        minutes = audio_duration / 60
        speech_rate = words / minutes

        # Define IELTS band score ranges for speech rate
        rate_ranges = {
            9: (150, 170),  # Optimal range
            8: (130, 190),
            7: (110, 210),
            6: (90, 230),
            5: (70, 250)
        }

        # Score based on speech rate
        base_score = self._score_within_ranges(speech_rate, rate_ranges)

        # Adjust for coherence using LLM
        coherence_adjustment = self._assess_coherence(response)

        return min(9.0, (base_score + coherence_adjustment) / 2)

    def _score_lexical(self, response: str) -> float:
        """Score lexical resource based on vocabulary range and accuracy"""
        prompt = f"""
        Analyze the following response for lexical resource according to IELTS criteria.
        Consider: vocabulary range, accuracy, and appropriateness.
        Response: {response}
        
        Rate from 0-9 and explain why.
        """

        # Get LLM analysis
        result = self._get_llm_analysis(prompt)
        return self._extract_score_from_analysis(result)

    def _score_grammar(self, response: str) -> float:
        """Score grammatical range and accuracy"""
        prompt = f"""
        Analyze the following response for grammatical accuracy and range according to IELTS criteria.
        Consider: sentence structures, tense usage, and error frequency.
        Response: {response}
        
        Rate from 0-9 and explain why.
        """

        return self._get_llm_analysis(prompt)

    def _score_pronunciation(self, response: str) -> float:
        """Score pronunciation using phonetic analysis"""
        # This would ideally use Azure Speech Services' pronunciation assessment
        # For now, we'll use a simplified LLM-based approach
        prompt = f"""
        Analyze the following response for pronunciation patterns according to IELTS criteria.
        Consider: word stress, intonation, and clarity.
        Response: {response}
        
        Rate from 0-9 and explain why.
        """

        return self._get_llm_analysis(prompt)

    async def _get_llm_analysis(self, prompt: str, max_retries: int = 3) -> float:
        """Get analysis from Azure OpenAI with retry logic"""
        for attempt in range(max_retries):
            try:
                # Add rate limiting check
                now = datetime.now()
                if 'analysis' in self.last_request_time:
                    time_since_last = (now - self.last_request_time['analysis']).total_seconds()
                    if time_since_last < self.min_request_interval:
                        await asyncio.sleep(self.min_request_interval - time_since_last)

                # Update last request time
                self.last_request_time['analysis'] = datetime.now()

                response = await self.client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[
                        {"role": "system", "content": "You are an IELTS examiner expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )
                return self._extract_score_from_analysis(response.choices[0].message.content)
            except Exception as e:
                if 'rate_limit' in str(e).lower() and attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                print(f"Error in LLM analysis (attempt {attempt+1}): {str(e)}")
                return 5.0
        return 5.0  # Default score if all retries failed

    def _generate_feedback(self, category: str, score: float, response: str) -> Dict:
        """Generate detailed feedback for a specific scoring category"""
        prompt = f"""
        Generate specific feedback for the following response in the {category} category.
        Score: {score}/9
        Response: {response}
        
        Provide:
        1. Specific improvements
        2. Examples of better alternatives
        3. Practice suggestions
        """

        feedback = self._get_llm_analysis(prompt)
        return {
            'score': score,
            'suggestions': self._parse_feedback(feedback),
            'examples': self._extract_examples(feedback)
        }

    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        weighted_sum = sum(
            scores[criterion] * weight
            for criterion, weight in self.criteria_weights.items()
        )
        return round(weighted_sum, 1)

    def _score_within_ranges(self, value: float, ranges: Dict[int, tuple]) -> float:
        """Helper function to score a value within defined ranges"""
        for score, (min_val, max_val) in ranges.items():
            if min_val <= value <= max_val:
                return float(score)
        return 5.0  # Default mid-range score

    def _assess_coherence(self, response: str) -> float:
        """Assess response coherence"""
        prompt = "Rate the coherence of this response from 0-9: " + response
        result = self._get_llm_analysis(prompt)
        return float(result) if isinstance(result, (int, float)) else 5.0

    def _extract_score_from_analysis(self, analysis: str) -> float:
        """Extract numerical score from LLM analysis"""
        try:
            import re
            matches = re.findall(r'\b[0-9](?:\.[0-9])?\b', str(analysis))
            return float(matches[0]) if matches else 5.0
        except:
            return 5.0

    def _parse_feedback(self, feedback: str) -> List[str]:
        """Parse feedback into suggestions list"""
        if not feedback:
            return []
        lines = str(feedback).split('\n')
        return [line.strip() for line in lines if line.strip()]

    def _extract_examples(self, feedback: str) -> List[str]:
        """Extract examples from feedback"""
        if not feedback:
            return []
        lines = str(feedback).split('\n')
        return [line for line in lines if 'example' in line.lower()]

    def _generate_fluency_feedback(self, response: str, score: float) -> Dict:
        return self._generate_feedback('fluency', score, response)

    def _generate_lexical_feedback(self, response: str, score: float) -> Dict:
        return self._generate_feedback('vocabulary', score, response)

    def _generate_grammar_feedback(self, response: str, score: float) -> Dict:
        return self._generate_feedback('grammar', score, response)

    def _generate_pronunciation_feedback(self, response: str, score: float) -> Dict:
        return self._generate_feedback('pronunciation', score, response)

class RequestRateLimiter:
    def __init__(self, requests_per_minute):
        self.requests_per_minute = requests_per_minute
        self.request_times = []
        self.min_interval = 60.0 / requests_per_minute

    async def wait_if_needed(self):
        now = datetime.datetime.now()
        # Remove old requests from history
        self.request_times = [t for t in self.request_times if (now - t).total_seconds() < 60]
        
        if len(self.request_times) >= self.requests_per_minute:
            oldest = min(self.request_times)
            wait_time = 60 - (now - oldest).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        self.request_times.append(now)
