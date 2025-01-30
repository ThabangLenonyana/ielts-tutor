import streamlit as st
import sounddevice as sd


def create_sidebar():
    """Create the sidebar with mode selection and settings"""

    with st.sidebar:
        st.title("IELTS Speaking Test")

        # Mode selection
        mode = st.radio(
            "Select Mode",
            ["Practice Mode", "Test Mode"],
            help="Practice Mode provides instant feedback. Test Mode simulates the full IELTS Speaking Test."
        )

        # Update session state
        st.session_state['mode'] = mode.lower().replace(" mode", "")

        st.divider()

        # Settings section
        st.subheader("Settings")

        # Microphone input selection if multiple devices
        devices = sd.query_devices()
        input_devices = [device['name']
                         for device in devices if device['max_input_channels'] > 0]
        audio_input = st.selectbox(
            "Select Microphone",
            input_devices,
            index=0
        )

        # Language preference for feedback (optional)
        feedback_lang = st.selectbox(
            "Feedback Language",
            ["English", "Spanish", "French", "Chinese"],
            index=0
        )

        st.divider()

        # Help section
        with st.expander("Help & Instructions"):
            st.markdown("""
            **Practice Mode:**
            - Get instant feedback after each response
            - Practice specific speaking skills
            - Review and retry questions
            
            **Test Mode:**
            - Complete 3-part IELTS speaking test
            - Timed responses
            - Comprehensive feedback at the end
            """)
