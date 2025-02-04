import streamlit as st
from pages.Home import main

st.set_page_config(
    page_title="IELTS Tutor",
    layout="wide",
    initial_sidebar_state="expanded"
)

if __name__ == "__main__":
    main()