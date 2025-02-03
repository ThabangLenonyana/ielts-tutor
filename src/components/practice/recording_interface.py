import streamlit as st
import logging
from modules.practice_manager import PracticeModeManager
from components.practice.chat_interface import update_conversation_history
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_recording_state():
    """Initialize session state variables for recording"""
    if 'audio_state' not in st.session_state:
        st.session_state.audio_state = {
            'processing': False,
            'last_processed': None,
            'recorded_audio': None
        }
    if 'practice_manager' not in st.session_state:
        st.session_state.practice_manager = PracticeModeManager()

async def render_recording_interface():
    init_recording_state()

    # Display recording widget
    audio_data = st.audio_input("Click to record your response", 
                               key=f"audio_recorder_{st.session_state.current_turn}",
                               help="Click to start/stop recording")
    
    if (audio_data is not None and 
        not st.session_state.audio_state['processing'] and 
        audio_data != st.session_state.audio_state['last_processed']):
        
        st.session_state.audio_state['processing'] = True
        st.session_state.audio_state['last_processed'] = audio_data
        await process_recorded_audio(audio_data)

async def process_recorded_audio(audio_data):
    """Process recorded audio and update conversation"""
    try:
        with st.spinner("Processing your response..."):
            success, result = await st.session_state.practice_manager.handle_response(audio_data)

        if success and result and 'transcription' in result:
            # Update conversation state
            update_conversation_history({
                'turn': st.session_state.current_turn,
                'question': st.session_state.current_question,
                'response': result['transcription'],
                'feedback': result['evaluation']
            })
            
            # Update session state
            st.session_state.transcription = result['transcription']
            st.session_state.feedback = result['evaluation']
            st.session_state.show_feedback_modal = True
            
            # Trigger UI update
            st.rerun()
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
    finally:
        st.session_state.audio_state['processing'] = False