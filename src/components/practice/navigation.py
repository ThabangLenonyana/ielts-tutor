import streamlit as st
import logging
from components.practice.session_state import advance_turn

logger = logging.getLogger(__name__)

async def render_navigation_buttons():
    """Render navigation buttons for practice mode"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("End Session", use_container_width=True):
            await _handle_end_session()
            
    with col2:
        if st.button("Next Question", type="primary", use_container_width=True):
            await _handle_next_question()

async def _handle_end_session():
    """Handle end session button click"""
    st.session_state.practice_active = False
    st.session_state.show_feedback_modal = False
    st.session_state.conversation_history = []
    st.rerun()

async def _handle_next_question():
    """Handle next question button click"""
    try:
        # Only proceed if feedback was shown for current turn
        if not st.session_state.get('show_feedback_modal'):
            st.warning("Please complete the current question first")
            return 
        
        # Advance to next turn
        advance_turn()
        
        # Get next question
        success, question = await st.session_state.practice_manager.get_next_question()
        if success:
            st.session_state.current_question = question
            st.rerun()
        else:
            st.error("Failed to get next question")
    except Exception as e:
        st.error(f"Error getting next question: {str(e)}")