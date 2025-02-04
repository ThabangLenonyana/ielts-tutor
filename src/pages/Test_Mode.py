import streamlit as st
from components.practice.session_state import init_session_state
from components.practice.sidebar import create_sidebar

def main():
    st.set_page_config(
        page_title="Test Mode",
        page_icon="📝",
        layout="wide"
    )
    
    create_sidebar()
    init_session_state('test')
    
    st.title("IELTS Speaking Test Mode")
    
    st.info("""
    The IELTS Speaking Test consists of 3 parts:
    1. Introduction and interview (4-5 minutes)
    2. Individual long turn (3-4 minutes) 
    3. Two-way discussion (4-5 minutes)
    """)
    
    if not st.session_state.test_active:
        if st.button("Start Test", type="primary"):
            st.session_state.test_active = True
            st.rerun()
    else:
        render_test_interface()

def render_test_interface():
    current_part = st.session_state.get('test_part', 1)
    
    # Show progress
    st.progress(current_part/3)
    st.caption(f"Part {current_part} of 3")
    
    # Render appropriate test section
    if current_part == 1:
        render_part_one()
    elif current_part == 2:
        render_part_two()
    else:
        render_part_three()

if __name__ == "__main__":
    main()