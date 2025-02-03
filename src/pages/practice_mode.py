import streamlit as st
from components.practice.session_state import init_session_state
from components.practice.topic_selector import render_topic_selector
from components.practice.recording_interface import render_recording_interface
from components.practice.chat_interface import render_chat_interface
from components.practice.feedback_display import render_feedback_modal
from components.practice.navigation import render_navigation_buttons


@st.dialog("Response Feedback", width='large')
def show_feedback_dialog():
    """Dialog function to display feedback"""
    if st.session_state.feedback:
        render_feedback_modal(st.session_state.feedback)


async def render_practice_mode():
        
    # Initialize state
    init_session_state()

    # Main content
    if not st.session_state.practice_active:
        await render_topic_selector()
    else:

        render_chat_interface()
        await render_recording_interface()

        # Add navigation buttons
        await render_navigation_buttons()

        # Show feedback modal if triggered
        if st.session_state.get('show_feedback_modal'):
            show_feedback_dialog()


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

@st.cache_resource
def get_async_recording_interface():
    return render_recording_interface()


