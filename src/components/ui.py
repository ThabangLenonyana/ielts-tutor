import streamlit as st


def create_main_ui():
    """Create the main UI based on selected mode"""

    st.title("IELTS Speaking Test Simulator")

    if st.session_state['mode'] == 'practice':
        _render_practice_mode()
    else:
        _render_test_mode()


def _create_topic_cards():
    """Create clickable topic cards with descriptions"""
    topics = {
        "Family": "Discuss your family members, relationships, and family life",
        "Work": "Talk about your job, career aspirations, and work experiences",
        "Education": "Share about your studies, learning experiences, and academic goals",
        "Hobbies": "Describe your interests, free-time activities, and pastimes",
        "Technology": "Discuss technology's impact on life, gadgets, and digital trends"
    }

    # Create columns for topic cards
    cols = st.columns(3)
    for idx, (topic, description) in enumerate(topics.items()):
        with cols[idx % 3]:
            # Create clickable card using HTML/CSS
            with st.container():
                st.markdown(f"""
                    <div style='padding: 1rem; 
                              border: 1px solid #E1E1E1; 
                              border-radius: 5px; 
                              margin: 0.5rem;'>
                        <h3>{topic}</h3>
                        <p>{description}</p>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("Select Topic", key=f"topic_{topic}"):
                    st.session_state['selected_topic'] = topic
                    st.session_state['practice_started'] = True
                    st.session_state['questions_answered'] = 0
                    st.rerun()


def _render_chat_interface():
    """Render the chat-like interface for practice session"""

    st.subheader(f"Practice Session: {st.session_state['selected_topic']}")

    # Sample questions for placeholder
    placeholder_questions = [
        "Tell me about your family.",
        "What do you enjoy doing in your free time?",
        "Describe your ideal job."
    ]

    # Chat container
    chat_container = st.container()
    with chat_container:
        # Display previous exchanges
        for q, a in st.session_state.get('conversation_history', []):
            with st.chat_message("assistant"):
                st.write(q)
            if a:
                with st.chat_message("user"):
                    st.write(a)

        # Current question
        current_q = placeholder_questions[st.session_state.get(
            'questions_answered', 0) % len(placeholder_questions)]
        with st.chat_message("assistant"):
            st.write(current_q)

        # Recording interface
        recording = st.session_state.get('recording', False)
        col1, col2 = st.columns([1, 3])

        with col1:
            if not recording:
                if st.button("🎤 Start Recording", use_container_width=True):
                    st.session_state['recording'] = True
                    st.rerun()
            else:
                if st.button("⏹️ Stop", type="primary", use_container_width=True):
                    st.session_state['recording'] = False
                    # Add placeholder response to conversation
                    response = "This is a placeholder for the transcribed response."
                    if 'conversation_history' not in st.session_state:
                        st.session_state['conversation_history'] = []
                    st.session_state['conversation_history'].append(
                        (current_q, response))
                    st.rerun()

        if recording:
            with col2:
                st.warning("Recording in progress...")

        # Show feedback after response
        if st.session_state.get('conversation_history'):
            _show_feedback(st.session_state['conversation_history'][-1][1])


def _show_feedback(response_text):
    """Display categorized feedback for the response"""
    st.divider()
    st.subheader("Response Feedback")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Grammar Corrections", expanded=True):
            st.write("• Suggested correction 1\n• Suggested correction 2")

        with st.expander("Vocabulary Suggestions", expanded=True):
            st.write("• Alternative word 1\n• Alternative phrase 2")

    with col2:
        with st.expander("Pronunciation Tips", expanded=True):
            st.write("• Pronunciation tip 1\n• Pronunciation tip 2")

        with st.expander("Fluency Assessment", expanded=True):
            st.progress(0.75)
            st.write("Fluency Score: 7.5/9")

    # Continue or End Practice
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue Practice"):
            st.session_state['questions_answered'] += 1
            # Placeholder for next question generation
    with col2:
        if st.button("End Practice"):
            st.session_state['practice_started'] = False
            st.session_state['show_summary'] = True


def _show_practice_summary():
    """Display practice session summary"""
    st.subheader("Practice Session Summary")

    st.markdown(f"""
    **Topic**: {st.session_state['selected_topic']}  
    **Questions Answered**: {st.session_state['questions_answered']}  
    **Overall Performance**:
    """)

    # Placeholder for overall scores
    scores = {
        "Grammar": 7.5,
        "Vocabulary": 7.0,
        "Pronunciation": 6.5,
        "Fluency": 7.0
    }

    for category, score in scores.items():
        st.write(f"{category}: {score}/9")


def _render_practice_mode():
    """Render the practice mode interface"""

    st.header("Practice Mode")


def _render_practice_mode():
    """Render the practice mode interface"""
    if not st.session_state.get('practice_started', False):
        st.info("Select a topic to begin your practice session:")
        _create_topic_cards()
    elif st.session_state.get('show_summary', False):
        _show_practice_summary()
    else:
        _render_chat_interface()


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
