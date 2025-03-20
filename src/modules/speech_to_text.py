import azure.cognitiveservices.speech as speechsdk
from typing import Tuple
import streamlit as st
import logging
import io
import wave
import numpy as np


class SpeechToText:
    """Handles speech-to-text conversion using Azure Speech Services"""

    def __init__(self):

        self.speech_key = 'B2iQAgBkwWi57F5UhDbtCIzsaIszhmuKc00D75G7d7V0aGlAp4fIJQQJ99BCACYeBjFXJ3w3AAAYACOGfofL'
        self.speech_region = 'eastus'
        self.logger = logging.getLogger(__name__)

        try:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            self.speech_config.speech_recognition_language = "en-US"
        except Exception as e:
            self.logger.error(f"Failed to initialize Speech Service: {str(e)}")
            raise RuntimeError(
                f"Failed to initialize Speech Service: {str(e)}")

    def transcribe_audio(self, audio_file) -> Tuple[bool, str]:
            
        try:
            audio_bytes = self.convert_audio_format(audio_file)

            audio_stream = speechsdk.audio.PushAudioInputStream()
            audio_stream.write(audio_bytes)
            audio_stream.close()

            audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )

            result = speech_recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return True, result.text
            else:
                self.logger.warning(f"Recognition failed: {result.reason}")
                return False, "No speech recognized"

        except Exception as e:
            self.logger.error(f"Transcription error: {str(e)}")
            return False, str(e)

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ["en-US", "en-GB", "en-AU"]  # Add more as needed

    def set_language(self, language_code: str) -> None:
        """Set recognition language"""
        if language_code in self.get_supported_languages():
            self.speech_config.speech_recognition_language = language_code


    def convert_audio_format(self, audio_file) -> bytes:
        """Convert audio to format required by Azure Speech SDK"""
        try:
            # Read input WAV file
            with wave.open(io.BytesIO(audio_file.read()), 'rb') as wav_file:
                # Get original parameters
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                
                # Read audio data
                audio_data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
                
                # Convert to mono if stereo
                if channels == 2:
                    audio_data = audio_data.reshape(-1, 2).mean(axis=1)

                # Resample to 16kHz if needed
                if framerate != 16000:
                    audio_data = self.resample(audio_data, framerate, 16000)
                
                # Convert to 16-bit PCM
                audio_data = audio_data.astype(np.int16)
                
                # Create output WAV file in memory
                output = io.BytesIO()
                with wave.open(output, 'wb') as out_wav:
                    out_wav.setnchannels(1)  # mono
                    out_wav.setsampwidth(2)  # 16-bit
                    out_wav.setframerate(16000)  # 16kHz
                    out_wav.writeframes(audio_data.tobytes())
                
                return output.getvalue()
                
        except Exception as e:
            self.logger.error(f"Audio conversion error: {str(e)}")
            raise

    def resample(self, audio_data: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """Resample audio data to target sample rate"""
        return np.interp(
            np.linspace(0, len(audio_data), int(len(audio_data) * target_sr / orig_sr)),
            np.arange(len(audio_data)),
            audio_data
        ).astype(np.int16)
    
