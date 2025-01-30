import streamlit as st


def _render_test_mode():
    """Render the test mode interface"""

    st.header("Test Mode")

    # Instructions
    st.info("""
    The IELTS Speaking Test consists of 3 parts:
    1. Introduction and interview (4-5 minutes)
    2. Individual long turn (3-4 minutes)
    3. Two-way discussion (4-5 minutes)
    """)

    # Start test button
    if st.button("Start Test"):
        st.subheader("Part 1: Introduction and Interview")

        # Timer
        st.write("Time remaining: 5:00")

        # Question
        st.write("First, let me ask you some questions about yourself.")

        # Record button
        st.button("🎤 Start Recording")

        # Response area
        st.empty()  # Placeholder for transcribed text

        # Progress
        st.progress(0.33)
        st.caption("Part 1 of 3")
