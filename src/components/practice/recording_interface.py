import streamlit as st
import numpy as np
from modules.audio_capture import AudioCapture
from components.practice.chat_interface import update_conversation_history


def render_recording_interface():
    col1, col2 = st.columns([1, 3])

    with col1:
        if not st.session_state.recording:
            if st.button("🎤 Start", type="primary", use_container_width=True):
                start_recording()
        else:
            if st.button("⏹️ Stop", type="primary", use_container_width=True):
                stop_recording()

    with col2:
        if st.session_state.recording:
            st.markdown("🔴 Recording...")


def start_recording():
    st.session_state.audio_capture = AudioCapture()
    success, msg = st.session_state.audio_capture.start()
    if success:
        st.session_state.recording = True

    else:
        st.error(msg)


def stop_recording():
    if 'audio_capture' not in st.session_state:
        st.error("No active recording session")
        return

    try:
        st.write("DEBUG: Stopping recording..")

        st.session_state.audio_capture.stop()
        st.session_state.recording = False

        audio_data = st.session_state.audio_capture.get_audio_data()

        if audio_data is not None:

            # Stop recording
            success, msg = st.session_state.audio_capture.stop()
            if not success:
                st.error(f"Failed to stop recording: {msg}")
                return

            st.session_state.audio_capture = None

            if audio_data is not None and len(audio_data) > 0:
                with st.spinner('Processing audio...'):
                    success, result = st.session_state.practice_manager.handle_response(
                        audio_data)

                    if success and result and 'transcription' in result:
                        st.write(
                            f"DEBUG: Got transcription: {result['transcription'][:30]}...")
                        st.session_state.feedback = result['evaluation']
                        st.session_state.transcription = result['transcription']
                        update_conversation_history(result['transcription'])

                    else:
                        st.error(
                            f"Failed to process audio: {result.get('error', 'Unknown error')}")
            else:
                st.error("No audio data captured")
    except Exception as e:
        st.error(f"Error in stop_recording: {str(e)}")
