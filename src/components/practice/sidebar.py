import streamlit as st


def create_sidebar():
    """Create the sidebar with settings only"""
    with st.sidebar:
        st.title("IELTS Speaking Test")
        
        # Settings section
        st.subheader("Settings")

        # Language preference for feedback (optional)
        feedback_lang = st.selectbox(
            "Feedback Language",
            ["English", "Spanish", "French", "Chinese"],
            index=0
        )

        st.divider()

        # Help section
        with st.expander("Help & Instructions"):
            st.markdown("""
            **Practice Mode:**
            - Get instant feedback after each response
            - Practice specific speaking skills
            - Review and retry questions
            
            **Test Mode:**
            - Complete 3-part IELTS speaking test
            - Timed responses
            - Comprehensive feedback at the end
            """)
