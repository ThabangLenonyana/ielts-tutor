import streamlit as st


def render_feedback_modal(feedback_data):
    with st.container():
        if 'evaluation_complete' not in st.session_state:
            with st.spinner('Analyzing your response...'):
                st.empty()

        st.markdown("### Your Response Analysis")

        # Scores in columns
        cols = st.columns(4)
        metrics = {
            "Fluency": feedback_data['scores']['fluency'],
            "Vocabulary": feedback_data['scores']['lexical'],
            "Grammar": feedback_data['scores']['grammar'],
            "Pronunciation": feedback_data['scores']['pronunciation']
        }

        for col, (category, score) in zip(cols, metrics.items()):
            with col:
                st.metric(category, f"{score:.1f}/9.0")

        # Detailed feedback
        st.markdown("### Detailed Feedback")
        for category, details in feedback_data['feedback'].items():
            st.markdown(f"**{category.title()}**")
            for suggestion in details['suggestions']:
                st.markdown(f"- {suggestion}")

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("End Session", use_container_width=True):
                st.session_state.practice_active = False
                st.session_state.show_feedback_modal = False
                st.session_state.conversation_history = []
                st.rerun()
        with col2:
            if st.button("Next Question", type="primary", use_container_width=True):
                if st.session_state.current_question and st.session_state.transcription:
                    exchange = {
                        'question': st.session_state.current_question,
                        'response': st.session_state.transcription
                    }
                    st.session_state.conversation_history.append(exchange)

                # Clear feedback state
                st.session_state.feedback = None
                st.session_state.show_feedback_modal = False
                st.session_state.transcription = None
                st.session_state.is_recording = False
                st.session_state.evaluation_complete = False

                # Get next question
                success, question = st.session_state.practice_manager.get_next_question()
                if success:
                    st.session_state.current_question = question
                st.rerun()
