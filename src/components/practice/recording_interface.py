import streamlit as st
import numpy as np
from modules.audio_capture import AudioCapture
from modules.practice_manager import PracticeModeManager
from components.practice.chat_interface import update_conversation_history


def init_recording_state():
    """Initialize session state variables for recording"""

    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'recorded_audio' not in st.session_state:
        st.session_state.recorded_audio = None
    if 'processing_state' not in st.session_state:
        st.session_state.processing_state = None
    if 'practice_manager' not in st.session_state:
        st.session_state.practice_manager = PracticeModeManager()


def render_recording_interface():
    init_recording_state()

    col1, col2 = st.columns([1, 3])

    with col1:
        if not st.session_state.is_recording:
            if st.button("🎤 Start", type="primary", use_container_width=True):
                handle_start_recording()
        else:
            if st.button("⏹️ Stop", type="primary", use_container_width=True):
                handle_stop_recording()

    with col2:
        if st.session_state.is_recording:
            st.markdown("Recording... 🔴 ")
        elif st.session_state.processing_state:
            st.markdown(f"⏳ {st.session_state.processing_state}")


def handle_start_recording():
    """Start audio recording and update UI state"""

    # st.session_state.is_recording = True
    # st.rerun()

    try:
        audio_capture = AudioCapture()
        success, msg = audio_capture.start()
        st.warning(
            f"DEBUG: Audio capture start result - Success: {success}, Message: {msg}")

        if success:
            st.session_state.audio_capture = audio_capture
            st.session_state.is_recording = True
            st.warning("DEBUG: Recording started successfully")

        else:
            st.error(f"Failed to start recording: {msg}")
            cleanup_recording_state()

    except Exception as e:
        st.error(f"Recording setup failed: {str(e)}")
        cleanup_recording_state()

    st.warning("DEBUG: Triggering rerun after recording start")
    st.rerun()


def handle_stop_recording():
    """Stop recording, capture audio data, and initiate processing"""
    try:
        # Check if we have an active recording session
        if not hasattr(st.session_state, 'audio_capture'):
            st.error("No active recording session")
            cleanup_recording_state()
            st.rerun()
            return

        # Stop recording and get audio data
        st.warning("DEBUG: Stopping audio capture")
        st.session_state.audio_capture.stop()
        audio_data = st.session_state.audio_capture.get_audio_data()
        st.warning(
            f"DEBUG: Audio data shape: {audio_data.shape if audio_data is not None else 'None'}")

        # Clean up recording state

        cleanup_recording_state()
        st.warning("DEBUG: Recording state cleaned up")

        if audio_data is not None and len(audio_data) > 0:
            st.session_state.processing_state = "Processing audio..."
            st.warning("DEBUG: Starting audio processing")

            process_recorded_audio(audio_data)
            st.rerun()  # Rerun to show processing state
        else:
            st.warning("No audio was recorded")
            st.rerun()

    except Exception as e:
        st.error(f"Error stopping recording: {str(e)}")
        cleanup_recording_state()
        st.rerun()


def process_recorded_audio(audio_data):
    """Process recorded audio and update conversation"""
    try:
        st.session_state.processing_state = "Processing audio..."

        success, result = st.session_state.practice_manager.handle_response(
            audio_data)
        st.warning(f"DEBUG: Transcription: {result['transcription'][:50]}...")

        if success and result and 'transcription' in result:
            st.session_state.feedback = result['evaluation']
            st.session_state.transcription = result['transcription']
            update_conversation_history(result['transcription'])
            st.warning("DEBUG: Conversation history updated")
        else:
            st.error(
                f"Failed to process audio: {result.get('error', 'Unknown error')}")

    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
    finally:
        st.session_state.processing_state = None
        st.warning("DEBUG: Processing complete, triggering rerun")

    # st.rerun()  # Rerun after processing is complete


def cleanup_recording_state():
    """Clean up recording-related session state"""
    st.session_state.is_recording = False
    if hasattr(st.session_state, 'audio_capture'):
        del st.session_state.audio_capture
