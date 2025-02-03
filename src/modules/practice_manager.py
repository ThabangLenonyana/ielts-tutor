from typing import Dict, List, Tuple
from .speech_to_text import SpeechToText
from .question_generator import QuestionGenerator
from .scoring import ScoringEngine
import logging
import wave
import asyncio


class PracticeModeManager:
    """Manages the IELTS speaking practice session flow"""

    def __init__(self):
        self.speech_to_text = SpeechToText()
        self.question_generator = QuestionGenerator()
        self.scoring_engine = ScoringEngine()
        self.session_state = self._get_default_session_state()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

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

    async def get_next_question(self) -> Tuple[bool, str]:
        """Generate next question based on topic and conversation history"""
        try:
            if not self.session_state or not self.session_state.get('active'):
                logging.error("No active session in get_next_question")
                return False, "No active session"

            # Get context from previous exchanges
            context = {
                'topic': self.session_state['current_topic'],
                'difficulty': self.session_state['current_difficulty'],
                'history': self.session_state.get('conversation_history', [])[-3:]
            }

            success, question = await self.question_generator.generate_question(
                context)
            logging.info(f"Generated question: {question}")
            if success:
                self.session_state['current_question'] = question
                return True, question
            
            logging.error(f"Question generation failed: {question}")
            return False, f"Failed to generate question"
        
        except Exception as e:
            return False, f"Error generating question: {str(e)}"

    async def handle_response(self, audio_file: bytes) -> Tuple[bool, Dict]:
        """Process user's spoken response"""
            
        try:
            if not hasattr(audio_file, 'read'):
                return False, {"error": "Invalid audio file"}
            
            original_position = audio_file.tell()

            self.logger.info("Starting transcription...")
            success, text = self.speech_to_text.transcribe_audio(audio_file)
            
            if not success:
                self.logger.error(f"Transcription failed: {text}")
                return False, {"error": "Failed to transcribe audio"}
            

            # reset position for duration calculation
            audio_file.seek(original_position)

            # Get audio duration from file
            with wave.open(audio_file, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                audio_duration = frames / float(rate)


            evaluation = await self.scoring_engine.evaluate_response(text, audio_duration)

            return True, {
                'transcription': text,
                'evaluation': evaluation,
                'audio_duration': audio_duration
            }

        except Exception as e:
            self.logger.error(f"Error in handle_response: {str(e)}")
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