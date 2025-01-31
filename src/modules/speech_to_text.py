import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
from typing import Tuple, Optional
import numpy as np
import streamlit as st


class SpeechToText:
    """Handles speech-to-text conversion using Azure Speech Services"""

    def __init__(self):
        load_dotenv()

        self.speech_key = st.secrets['SPEECH_API_KEY']
        self.speech_region = st.secrets['SPEECH_REGION']

        if not self.speech_key or not self.speech_region:
            raise ValueError(
                "Azure Speech credentials not found in environment")

        try:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            self.speech_config.speech_recognition_language = "en-US"
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Speech Service: {str(e)}")

    def transcribe_audio(self, audio_data: np.ndarray) -> Tuple[bool, str]:
        """Transcribe audio data to text"""
        try:
            # Validate audio data
            if audio_data is None or audio_data.size == 0:
                return False, "No audio data provided"

            # Convert float32 audio to int16
            audio_int16 = (audio_data * 32768).astype(np.int16)

            # Create audio stream from numpy array
            audio_stream = speechsdk.audio.PushAudioInputStream()
            audio_stream.write(audio_int16.tobytes())
            audio_stream.close()

            # Create audio config
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, region=self.speech_region)
            audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)

            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )

            # Start recognition
            result = speech_recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return True, result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return False, f"No speech could be recognized: {result.no_match_details}"
            elif result.reason == speechsdk.ResultReason.Canceled:
                return False, f"Speech Recognition canceled: {result.cancellation_details.reason}"

        except Exception as e:
            return False, f"Error during transcription: {str(e)}"

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ["en-US", "en-GB", "en-AU"]  # Add more as needed

    def set_language(self, language_code: str) -> None:
        """Set recognition language"""
        if language_code in self.get_supported_languages():
            self.speech_config.speech_recognition_language = language_code
