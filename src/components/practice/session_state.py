import streamlit as st
from modules.practice_manager import PracticeModeManager

def reset_turn_state():
    """Reset all turn-specific state variables"""
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
    """Prepare for next turn"""
    if st.session_state.get('show_feedback_modal'):
        st.session_state.current_turn += 1
        reset_turn_state()
    else:
        st.warning("Please complete the current question first")

def init_session_state():
    # Initialize practice manager
    if 'practice_manager' not in st.session_state:
        st.session_state.practice_manager = PracticeModeManager()

    # Session-level state (persists across turns)
    session_state = {
        'practice_active': False,
        'current_topic': None,
        'conversation_history': [],
        'current_turn': 0,
        'current_question': None
    }

    for key, value in session_state.items():
        if key not in st.session_state:
            st.session_state[key] = value