import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_chat_interface():
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header(f"Practice Mode")

    with col2:
        st.markdown(
            f"""
            <style>
            .stButton>button[disabled] {{
                color: #ff4b4b;
                border: 2px solid #ff4b4b;
                width: 100%;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.button(st.session_state.current_topic, disabled=True)

    st.divider()
    
    # Add debugging information
    if st.checkbox("Show Debug Info"):
        st.write("Session State:", {
            'practice_active': st.session_state.get('practice_active'),
            'current_topic': st.session_state.get('current_topic'),
            'current_question': st.session_state.get('current_question'),
            'current_turn': st.session_state.get('current_turn')
        })

    if not st.session_state.get('current_question'):
        logger.error("No question available in session state")
        st.error("No question available")
        return

    chat_container = st.container()

    with chat_container:
        for exchange in st.session_state.conversation_history:
            with st.chat_message("assistant"):
                st.caption(f"Turn {exchange['turn'] + 1}")
                st.write(exchange['question'])
            if exchange.get('response'):
                with st.chat_message("user"):
                    st.write(exchange['response'])

        # Show current question only if not in conversation history
        if (st.session_state.current_question and 
            (not st.session_state.conversation_history or 
             st.session_state.current_question != st.session_state.conversation_history[-1].get('question'))):
            with st.chat_message("assistant"):
                st.caption(f"Turn {st.session_state.current_turn + 1}")
                st.write(st.session_state.current_question)


def update_conversation_history(exchange_data):
    """Update conversation history with new exchange"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    st.session_state.conversation_history.append(exchange_data)
