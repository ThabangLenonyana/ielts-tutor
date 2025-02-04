import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_turn_feedback(turn, feedback_data):
    """Click handler for feedback buttons"""
    st.session_state.selected_turn_feedback = turn
    st.session_state.selected_turn_feedback = feedback_data
    st.session_state.show_feedback_modal = True


def render_chat_interface():
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header(f"Practice Mode", divider='rainbow')

    with col2:
        st.markdown(
            f"""
            <style>
            .stButton>button[disabled] {{
                color: #ff4b4b;
                border: 2px solid #ff4b4b;
                width: 100%;
            }}
            .feedback-btn {{
                padding: 0.25rem 0.75rem;
                font-size: 0.8em;
                opacity: 0.8;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.button(st.session_state.current_topic, disabled=True)

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
                cols = st.columns([0.9, 0.1])
                with cols[0]:
                    with st.chat_message("user"):
                        st.write(exchange['response'])
                
                with cols[1]:
                    if exchange.get('feedback'):
                        st.button(
                            "📊",
                            key=f"feedback_btn_{exchange['turn']}",
                            on_click=show_turn_feedback,
                            args=(exchange['turn'], exchange['feedback']),
                            type="secondary",
                            use_container_width=True,
                            
                        
                        )

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