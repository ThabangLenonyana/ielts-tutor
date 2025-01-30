import streamlit as st


def render_topic_selector():
    st.title("IELTS Speaking Practice")
    st.subheader("Select a Topic")

    topics = {
        "Work": "💼",
        "Education": "📚",
        "Technology": "💻",
        "Environment": "🌍",
        "Travel": "✈️"
    }

    cols = st.columns(3)
    for idx, (topic, emoji) in enumerate(topics.items()):
        with cols[idx % 3]:
            if st.button(f"{emoji} {topic}", key=f"topic_{idx}", use_container_width=True):
                start_practice_session(topic)


def start_practice_session(topic):
    st.session_state.practice_manager.start_session(topic)
    st.session_state.practice_active = True
    st.session_state.current_topic = topic

    # Get initial question
    success, question = st.session_state.practice_manager.get_next_question()
    if success:
        st.session_state.current_question = question
    st.rerun()
