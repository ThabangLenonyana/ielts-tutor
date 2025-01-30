from modules.speech_to_text import SpeechToText
from modules.audio_capture import AudioCapture
import sys
import os
import time
import numpy as np
from pathlib import Path

# Add src to Python path
# Add parent directory to path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))


def test_audio_capture():
    print("Starting audio capture test...")

    # Initialize components
    audio_capture = AudioCapture()
    speech_to_text = SpeechToText()

    try:
        # Start recording
        success, msg = audio_capture.start()
        if not success:
            print(f"Failed to start recording: {msg}")
            return

        print("Recording for 5 seconds...")
        time.sleep(5)  # Record for 5 seconds

        # Stop recording
        audio_capture.stop()
        print("Recording stopped")

        # Get audio data
        audio_data = audio_capture.get_audio_data()
        if audio_data is None:
            print("No audio data captured")
            return

        print(f"Audio data shape: {audio_data.shape}")
        print(
            f"Audio duration: {len(audio_data)/audio_capture.sample_rate:.2f}s")

        # Test transcription
        print("Transcribing audio...")
        success, transcription = speech_to_text.transcribe_audio(audio_data)

        if success:
            print(f"Transcription successful: {transcription}")
        else:
            print(f"Transcription failed: {transcription}")

    except Exception as e:
        print(f"Test failed with error: {str(e)}")
    finally:
        if hasattr(audio_capture, 'stream'):
            audio_capture.stop()


if __name__ == "__main__":
    test_audio_capture()
