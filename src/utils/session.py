import streamlit as st


def init_session_state():
    """Initialize session state variables"""
    if 'mode' not in st.session_state:
        st.session_state['mode'] = 'practice'

    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = None

    if 'selected_topic' not in st.session_state:
        st.session_state['selected_topic'] = None

    if 'practice_started' not in st.session_state:
        st.session_state['practice_started'] = False

    if 'questions_answered' not in st.session_state:
        st.session_state['questions_answered'] = 0

    if 'recording' not in st.session_state:
        st.session_state['recording'] = False

    if 'show_summary' not in st.session_state:
        st.session_state['show_summary'] = False
