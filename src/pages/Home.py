import streamlit as st
from components.practice.sidebar import create_sidebar



def main():
    st.set_page_config(
        page_title="IELTS Speaking Test Simulator ",
        page_icon="🎯",
        layout="wide"
    )
    
    create_sidebar()
    
    container_col1, container_col2, container_col3 = st.columns([1,4,1])
    # Header container with background
    with container_col2:
        with st.container():
            st.header("Welcome to the Speaking Test Simulator 🎯", divider='rainbow' )
        

        # Quick Stats
        st.subheader("📊 Your Progress")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Practice Sessions", value="12", delta="↑2 this week")
        with col2:
            st.metric(label="Average Score", value="6.5", delta="↑0.5")
        with col3:
            st.metric(label="Topics Covered", value="8/20", delta="40%")
        with col4:
            st.metric(label="Speaking Time", value="120 min", delta="↑15 min")
        
        # Mode Selection
        st.markdown("---")
        st.subheader("Choose Your Mode")
        
        mode_col1, mode_col2 = st.columns(2, gap="large")
        
        with mode_col1:
            st.markdown("### Practice Mode 🎯")
            st.info("""
            - Choose specific topics
            - Get instant feedback
            - Practice at your own pace
            - Review and retry questions
            """)
            st.page_link("pages/Practice_Mode.py", label="Start Practice", use_container_width=True)
        
        with mode_col2:
            st.markdown("### Test Mode 📝")
            st.info("""
            - Complete 3-part test
            - Timed sections
            - Real test conditions
            - Full evaluation report
            """)
            st.page_link("pages/Test_Mode.py", label="Start Test", use_container_width=True)
        
        # Recent Activity
        st.markdown("---")
        recent_col1, recent_col2 = st.columns(2, gap="large")
        
        with recent_col1:
            st.subheader("📋 Recent Activity")
            activity_data = [
                {"date": "Today", "topic": "Work & Career", "score": "6.5"},
                {"date": "Yesterday", "topic": "Education", "score": "7.0"},
                {"date": "3 days ago", "topic": "Technology", "score": "6.0"}
            ]
            st.table(activity_data)
        
        with recent_col2:
            st.subheader("🎯 Focus Areas")
            st.progress(75, text="Fluency")
            st.progress(60, text="Vocabulary")
            st.progress(80, text="Pronunciation")
            st.progress(70, text="Grammar")


def check_secrets():
    """Verify all required secrets are available"""
    required_secrets = [
        "SPEECH_API_KEY",
        "SPEECH_REGION",
        "MODEL_API_KEY",
        "MODEL_URI"
    ]

    missing_secrets = [
        secret for secret in required_secrets if secret not in st.secrets]

    if missing_secrets:
        st.error(f"Missing required secrets: {', '.join(missing_secrets)}")
        st.stop()



if __name__ == "__main__":
    main()