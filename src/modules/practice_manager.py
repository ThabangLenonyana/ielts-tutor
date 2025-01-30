from typing import Dict, List, Tuple, Optional
from .speech_to_text import SpeechToText
from .audio_capture import AudioCapture
from .question_generator import QuestionGenerator
from .scoring import ScoringEngine
import numpy as np


class PracticeModeManager:
    """Manages the IELTS speaking practice session flow"""

    def __init__(self):
        self.speech_to_text = SpeechToText()
        self.audio_capture = AudioCapture()
        self.question_generator = QuestionGenerator()
        self.scoring_engine = ScoringEngine()

        self.session_state = self._get_default_session_state()

    def _get_default_session_state(self) -> Dict:
        """Initialize default session state with all required fields"""
        return {
            'active': False,
            'current_topic': None,
            'questions_answered': 0,
            'conversation_history': [],
            'current_difficulty': 1.0,
            'feedback_history': [],
            'current_question': None,
            'duration': 0
        }

    def start_session(self, topic: str) -> bool:
        """Initialize a new practice session"""
        try:
            if not topic:
                return False
            self.session_state = self._get_default_session_state()
            self.session_state.update({
                'active': True,
                'current_topic': topic,
            })
            return True
        except Exception as e:
            print(f"Error starting session: {str(e)}")
            return False

    def get_next_question(self) -> Tuple[bool, str]:
        """Generate next question based on topic and conversation history"""
        try:
            if not self.session_state or not self.session_state.get('active'):
                return False, "No active session"

            # Get context from previous exchanges
            context = {
                'topic': self.session_state['current_topic'],
                'difficulty': self.session_state['current_difficulty'],
                'history': self.session_state['conversation_history'][-3:] if self.session_state['conversation_history'] else []
            }

            success, question = self.question_generator.generate_question(
                context)
            if success:
                return True, question
            return False, f"Failed to generate question"
        except Exception as e:
            return False, f"Error generating question: {str(e)}"

    def handle_response(self, audio_data: np.ndarray) -> Tuple[bool, Dict]:
        """Process user's spoken response"""
        try:
            print(
                f"DEBUG: Handling response - Audio shape: {audio_data.shape}")

            # Transcribe audio
            print("DEBUG: Starting transcription...")
            success, text = self.speech_to_text.transcribe_audio(audio_data)
            print(
                f"DEBUG: Transcription result: {success}, {text[:30] if success else 'Failed'}")

            if not success:
                return False, {"error": "Failed to transcribe audio"}

            # Generate feedback
            audio_duration = len(audio_data) / self.audio_capture.sample_rate
            evaluation = self.scoring_engine.evaluate_response(
                text, audio_duration)

            # Update session state
            self.session_state['questions_answered'] += 1
            self.session_state['conversation_history'].append({
                'question': self.session_state.get('current_question', "Unknown"),
                'response': text,
                'feedback': evaluation
            })

            return True, {
                'transcription': text,
                'evaluation': evaluation,
                'audio_duration': audio_duration
            }
        except Exception as e:
            return False, {"error": str(e)}

    def get_session_summary(self) -> Dict:
        """Generate end-of-session summary"""

        if not self.session_state['conversation_history']:
            return {"error": "No practice data available"}

        # Calculate average scores
        scores = {
            'grammar': 0,
            'vocabulary': 0,
            'pronunciation': 0,
            'fluency': 0
        }

        for exchange in self.session_state['conversation_history']:
            feedback = exchange['feedback']
            for category in scores:
                scores[category] += feedback[category]['score']

        total_responses = len(self.session_state['conversation_history'])
        for category in scores:
            scores[category] /= total_responses

        return {
            'topic': self.session_state['current_topic'],
            'questions_answered': self.session_state['questions_answered'],
            'average_scores': scores,
            'improvement_areas': self._identify_improvement_areas(scores),
            'practice_duration': self.session_state.get('duration', 0)
        }

    def _identify_improvement_areas(self, scores: Dict) -> List[str]:
        """Identify areas needing most improvement"""
        weak_areas = []
        for category, score in scores.items():
            if score < 6.5:  # IELTS benchmark
                weak_areas.append(category)
        return weak_areas

    def end_session(self) -> Dict:
        """End the practice session and return summary"""
        summary = self.get_session_summary()
        self.session_state['active'] = False
        return summary

    def _adjust_difficulty(self, score: float):
        """Adjust difficulty based on performance"""
        # Convert IELTS score (0-9) to difficulty adjustment
        normalized_score = score / 9.0
        adjustment = 0.1 * (normalized_score - 0.5)
        new_difficulty = self.session_state['current_difficulty'] + adjustment
        # Clamp difficulty between 0-2
        self.session_state['current_difficulty'] = max(
            0.0, min(2.0, new_difficulty))
