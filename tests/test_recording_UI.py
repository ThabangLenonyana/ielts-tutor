import numpy as np
import streamlit as st
import pytest
from src.components.practice.recording_interface import (
    init_recording_state,
    handle_start_recording,
    handle_stop_recording,
    process_recorded_audio,
    cleanup_recording_state
)


class MockAudioCapture:
    def __init__(self, mock_audio_data=None):
        self.is_recording = False
        self.mock_audio_data = mock_audio_data or np.zeros(1000)

    def start(self):
        self.is_recording = True
        return True, "Started successfully"

    def stop(self):
        self.is_recording = False

    def get_audio_data(self):
        return self.mock_audio_data


class MockPracticeModeManager:
    def handle_response(self, audio_data):
        return True, {
            'transcription': 'Test transcription',
            'evaluation': 'Test feedback'
        }


@pytest.fixture
def setup_session_state(monkeypatch):
    # Reset session state before each test
    if hasattr(st, '_is_running_with_streamlit'):
        st.session_state.clear()
    init_recording_state()

    # Mock AudioCapture
    monkeypatch.setattr(
        'components.practice.recording_interface.AudioCapture', MockAudioCapture)
    # Mock PracticeModeManager
    st.session_state.practice_manager = MockPracticeModeManager()


def test_recording_flow(setup_session_state):
    """Test the complete recording flow"""
    # Initial state
    assert not st.session_state.is_recording
    assert st.session_state.processing_state is None

    # 1. Start Recording
    handle_start_recording()
    assert st.session_state.is_recording
    assert hasattr(st.session_state, 'audio_capture')

    # 2. Stop Recording
    handle_stop_recording()
    assert not st.session_state.is_recording
    assert not hasattr(st.session_state, 'audio_capture')
    assert st.session_state.processing_state == "Processing audio..."

    # 3. Check Feedback
    assert hasattr(st.session_state, 'feedback')
    assert hasattr(st.session_state, 'transcription')
    assert st.session_state.processing_state is None


def test_start_recording_state(setup_session_state):
    """Test start recording button state changes"""
    handle_start_recording()
    assert st.session_state.is_recording
    assert hasattr(st.session_state, 'audio_capture')


def test_stop_recording_state(setup_session_state):
    """Test stop recording button state changes"""
    # Setup recording state
    handle_start_recording()

    # Stop recording
    handle_stop_recording()
    assert not st.session_state.is_recording
    assert not hasattr(st.session_state, 'audio_capture')
    assert st.session_state.processing_state == "Processing audio..."


def test_audio_processing_state(setup_session_state):
    """Test audio processing state transitions"""
    mock_audio_data = np.zeros(1000)
    process_recorded_audio(mock_audio_data)

    assert hasattr(st.session_state, 'feedback')
    assert hasattr(st.session_state, 'transcription')
    assert st.session_state.processing_state is None


def test_cleanup_state(setup_session_state):
    """Test cleanup of recording state"""
    # Setup recording state
    handle_start_recording()

    # Cleanup
    cleanup_recording_state()
    assert not st.session_state.is_recording
    assert not hasattr(st.session_state, 'audio_capture')


def test_error_handling(setup_session_state, monkeypatch):
    """Test error handling during recording"""
    # Mock AudioCapture to fail
    class FailingAudioCapture:
        def start(self):
            return False, "Failed to start"

    monkeypatch.setattr(
        'components.practice.recording_interface.AudioCapture', FailingAudioCapture)

    handle_start_recording()
    assert not st.session_state.is_recording
    assert not hasattr(st.session_state, 'audio_capture')
