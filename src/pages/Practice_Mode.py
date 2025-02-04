import streamlit as st
from components.practice.session_state import init_session_state
from components.practice.topic_selector import render_topic_selector
from components.practice.recording_interface import render_recording_interface
from components.practice.chat_interface import render_chat_interface
from components.practice.feedback_display import render_feedback_modal
from components.practice.navigation import render_navigation_buttons
from components.practice.sidebar import create_sidebar

async def main():
    st.set_page_config(
        page_title="Practice Mode",
        page_icon="🎯",
        layout="wide"
    )
    
    create_sidebar()
    init_session_state('practice')

    container_col1, container_col2, container_col3 = st.columns([1,4,1])
    
    with container_col2:
       
        
        # Main content
        if not st.session_state.practice_active:
            st.header("Practice Mode", divider='rainbow')
            await render_topic_selector()
        else:
            render_chat_interface()
            await render_recording_interface()
            await render_navigation_buttons()
            
            if st.session_state.get('show_feedback_modal'):
                show_feedback_dialog()

@st.dialog("Response Feedback", width='large')
def show_feedback_dialog():
    if st.session_state.feedback:
        render_feedback_modal(st.session_state.feedback)
    if st.session_state.get('selected_turn_feedback'):
        render_feedback_modal(st.session_state.selected_turn_feedback)
        if st.button("Close"):
            st.session_state.show_feedback_modal = False
            st.session_state.selected_turn_feedback = None

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())