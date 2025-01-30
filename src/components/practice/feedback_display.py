import streamlit as st


def render_feedback(feedback_data):
    st.subheader("Feedback")

    # Scores
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
    with st.expander("Detailed Feedback", expanded=True):
        for category, details in feedback_data['feedback'].items():
            st.markdown(f"**{category.title()}**")
            for suggestion in details['suggestions']:
                st.markdown(f"- {suggestion}")
