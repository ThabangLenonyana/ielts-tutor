import streamlit as st
from components.practice.session_state import reset_turn_state


async def render_topic_selector():
    st.title("IELTS Speaking Practice")
    st.subheader("Select a Topic")

    topics = {
        "Work": "💼",
        "Education": "📚",
        "Technology": "💻",
        "Environment": "🌍",
        "Travel": "✈️",
        "Health": "🏥",
        "Culture": "🎨",
        "Food": "🍔",
        "Sports": "⚽",
    }

    cols = st.columns(3)
    for idx, (topic, emoji) in enumerate(topics.items()):
        with cols[idx % 3]:
            if st.button(f"{emoji} {topic}", key=f"topic_{idx}", use_container_width=True):
                await start_practice_session(topic)


async def start_practice_session(topic):
    """Initialize practice session with first question"""
    st.session_state.practice_manager.start_session(topic)
    st.session_state.practice_active = True
    st.session_state.current_topic = topic
    st.session_state.current_turn = 0
    reset_turn_state()

    # Get initial question
    success, question = await st.session_state.practice_manager.get_next_question()
    if success:
        st.session_state.current_question = question
        st.rerun()
    else:
        st.error("Failed to get initial question")
    # st.rerun()
