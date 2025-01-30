import streamlit as st
from pages.practice_mode import render_practice_mode
from components.test_mode.test_mode import _render_test_mode
from components.practice.sidebar import create_sidebar
from components.practice.session_state import init_session_state


def main():
    # Initialize session state
    init_session_state()

    # Create sidebar
    create_sidebar()

    # Create main UI
    create_main_ui()


def create_main_ui():
    """Create the main UI based on selected mode"""

    st.title("IELTS Speaking Test Simulator")

    # Initialize session state
    init_session_state()

    if st.session_state['mode'] == 'practice':
        render_practice_mode()
    else:
        _render_test_mode()


if __name__ == "__main__":
    main()
