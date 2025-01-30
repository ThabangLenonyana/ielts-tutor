import sounddevice as sd
import numpy as np
import queue
from typing import Optional, Tuple


class AudioCapture:
    """Handles real-time audio capture from microphone"""

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.state = 'initialized'
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_queue = queue.Queue()
        self.stream = None
        self.is_recording = False

    def callback(self, indata: np.ndarray, frames: int, time, status) -> None:
        """Callback function for the audio stream"""
        if status:
            print(f'Audio callback error: {status}')
        self.audio_queue.put(indata.copy())

    def start(self) -> Tuple[bool, str]:
        """Start audio capture"""
        try:
            if self.state != 'initialized':
                return False, "Invalid state for starting recording"

            self.stream = sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                callback=self.callback
            )

            self.stream.start()
            self.is_recording = True
            self.state = 'recording'
            return True, "Recording started successfully"
        except Exception as e:
            return False, f"Error starting audio capture: {str(e)}"

    def stop(self) -> Tuple[bool, str]:
        """Stop audio capture"""
        if self.state != 'recording':
            return False, "Not currently recording"

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.is_recording = False
            self.state = 'stopped'
            return True, "Recording stopped successfully"
        return False, "No active recording to stop"

    def get_audio_data(self) -> Optional[np.ndarray]:
        """Get accumulated audio data from the queue"""
        data = []
        while not self.audio_queue.empty():
            data.append(self.audio_queue.get())
        return np.vstack(data) if data else None

    def clear_queue(self) -> None:
        """Clear the audio queue"""
        while not self.audio_queue.empty():
            self.audio_queue.get()
