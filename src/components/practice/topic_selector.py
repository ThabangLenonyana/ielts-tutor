import streamlit as st
from components.practice.session_state import reset_turn_state


async def render_topic_selector():
    st.subheader("Select a Topic")

    # Add custom CSS for consistent button sizing
    st.markdown("""
        <style>
        .topic-button {
            min-height: 80px;
            height: 100%;
            white-space: normal;
            position: relative;
        }
        </style>
    """, unsafe_allow_html=True)

    topics = {
        "Work": {
            "emoji": "💼",
            "description": "Career, workplace, and professional life topics"
        },
        "Education": {
            "emoji": "📚",
            "description": "Learning, schools, and academic subjects"
        },
        "Technology": {
            "emoji": "💻",
            "description": "Digital innovation, gadgets, and modern tech"
        },
        "Environment": {
            "emoji": "🌍",
            "description": "Nature, climate change, and sustainability"
        },
        "Travel": {
            "emoji": "✈️",
            "description": "Tourism, destinations, and cultural experiences"
        },
        "Health": {
            "emoji": "🏥",
            "description": "Wellness, medical care, and lifestyle"
        },
        "Culture": {
            "emoji": "🎨",
            "description": "Arts, traditions, and social customs"
        },
        "Food": {
            "emoji": "🍔",
            "description": "Cuisine, cooking, and dining habits"
        },
        "Sports": {
            "emoji": "⚽",
            "description": "Athletics, games, and physical activities"
        },
    }

    cols = st.columns(3)
    for idx, (topic, info) in enumerate(topics.items()):
        with cols[idx % 3]:
            button_label = f"{info['emoji']} {topic}"
            help_text = info['description']
            if st.button(
                button_label, 
                key=f"topic_{idx}", 
                help=help_text,
                use_container_width=True
            ):
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
