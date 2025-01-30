import streamlit as st
from components.practice.session_state import init_session_state
from components.practice.topic_selector import render_topic_selector
from components.practice.recording_interface import render_recording_interface
from components.practice.chat_interface import render_chat_interface
from components.practice.feedback_display import render_feedback


def render_practice_mode():

    # Initialize state
    init_session_state()

    # Main content
    if not st.session_state.practice_active:
        render_topic_selector()
    else:

        render_chat_interface()
        render_recording_interface()

        st.divider()

        if st.session_state.feedback:
            render_feedback(st.session_state.feedback)


def end_practice_session() -> None:
    """End the current practice session and display summary"""
    if 'practice_manager' in st.session_state:
        # Get session summary
        summary = st.session_state.practice_manager.end_session()

        # Display summary
        st.markdown("## Session Summary")
        st.markdown(f"**Topic:** {summary['topic']}")
        st.markdown(f"**Questions Answered:** {summary['questions_answered']}")

        # Display average scores
        for category, score in summary['average_scores'].items():
            st.metric(f"{category.title()}", f"{score:.1f}/9.0")

        # Display improvement areas
        if summary['improvement_areas']:
            st.markdown("### Areas for Improvement")
            for area in summary['improvement_areas']:
                st.markdown(f"- {area}")

        # Reset session state
        st.session_state.practice_active = False
        st.session_state.current_topic = None
        st.session_state.current_question = None
        st.session_state.conversation_history = []
        st.session_state.feedback = None

        # Force page refresh
        st.rerun()


if __name__ == "__main__":
    render_practice_mode()
