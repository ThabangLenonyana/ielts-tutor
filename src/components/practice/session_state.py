import streamlit as st
from modules.practice_manager import PracticeModeManager

def init_session_state(mode: str):
    """Initialize session state based on mode"""
    if mode == 'practice':
        init_practice_state()
    elif mode == 'test':
        init_test_state()

def init_practice_state():
    """Initialize practice mode state"""
    if 'practice_manager' not in st.session_state:
        st.session_state.practice_manager = PracticeModeManager()

    practice_state = {
        'practice_active': False,
        'current_topic': None,
        'conversation_history': [],
        'current_turn': 0,
        'current_question': None,
        'audio_state': {
            'processing': False,
            'last_processed': None,
            'recorded_audio': None
        }
    }

    for key, value in practice_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_test_state():
    """Initialize test mode state"""
    test_state = {
        'test_active': False,
        'test_part': 1,
        'timer': 0,
        'responses': [],
        'current_question': None,
        'test_complete': False,
        'audio_state': {
            'processing': False,
            'last_processed': None,
            'recorded_audio': None
        }
    }

    for key, value in test_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_turn_state():
    """Reset turn-specific state variables"""
    st.session_state.audio_state = {
        'processing': False,
        'last_processed': None,
        'recorded_audio': None
    }
    st.session_state.transcription = None
    st.session_state.feedback = None
    st.session_state.show_feedback_modal = False
    st.session_state.turn_complete = False

def advance_turn():
    """Advance to next turn in practice mode"""
    if st.session_state.get('show_feedback_modal'):
        st.session_state.current_turn += 1
        reset_turn_state()
    else:
        st.warning("Please complete the current question first")