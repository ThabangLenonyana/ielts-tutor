import streamlit as st
from components.ui import create_main_ui
from components.sidebar import create_sidebar
from utils.session import init_session_state


def main():
    # Initialize session state
    init_session_state()

    # Create sidebar
    create_sidebar()

    # Create main UI
    create_main_ui()


if __name__ == "__main__":
    main()
