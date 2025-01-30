import streamlit as st
from modules.practice_manager import PracticeModeManager


def init_session_state():
    # Initialize practice manager if not exists
    if 'practice_manager' not in st.session_state:
        st.session_state.practice_manager = PracticeModeManager()

    if 'audio_capture' not in st.session_state:
        st.session_state.audio_capture = None

    # Initialize all required state variables
    if 'practice_active' not in st.session_state:
        st.session_state.practice_active = False

    if 'recording' not in st.session_state:
        st.session_state.recording = False

    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None

    if 'current_question' not in st.session_state:
        st.session_state.current_question = None

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'transcription' not in st.session_state:
        st.session_state.transcription = None

    if 'feedback' not in st.session_state:
        st.session_state.feedback = None

    if 'last_response' not in st.session_state:
        st.session_state.last_response = None
