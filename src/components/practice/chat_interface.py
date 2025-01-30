import streamlit as st


def render_chat_interface():
    st.subheader(f"Topic: {st.session_state.current_topic}")

    chat_container = st.container()

    with chat_container:
        for exchange in st.session_state.conversation_history:
            with st.chat_message("assistant"):
                st.write(exchange['question'])
            if exchange.get('response'):
                with st.chat_message("user"):
                    st.write(exchange['response'])

        if st.session_state.current_question:
            with st.chat_message("assistant"):
                st.write(st.session_state.current_question)


def update_conversation_history(response_text):
    try:
        st.write("DEBUG: Updating conversation history...")
        st.write(
            f"DEBUG: Current question: {st.session_state.current_question}")

        if not response_text:
            st.warning("Empty response text recieved")

        if st.session_state.current_question:
            exchange = {
                'question': st.session_state.current_question,
                'response': response_text
            }

            # Append to history
            if 'conversation_history' not in st.session_state:
                st.write("DEBUG: Initializing conversation history...")
                st.session_state.conversation_history = []
                st.write(
                    f"DEBUG: Appending exchange to history. History length: {len(st.session_state.conversation_history)}")

            st.session_state.conversation_history.append(exchange)

            # Get next question
            success, question = st.session_state.practice_manager.get_next_question()
            if success:
                st.write(f"DEBUG: Got next question: {question}")
                st.session_state.current_question = question
            else:
                st.write("DEBUG: No more questions available")
                st.session_state.current_question = None
        else:
            st.warning("No current question found in session state")
    except Exception as e:
        st.error(f"Failed to update conversation history: {str(e)}")
