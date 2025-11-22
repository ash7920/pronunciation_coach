import streamlit as st

def show_header():
    st.title("🎧 Pronunciation Coach")
    st.write("Improve your pronunciation with AI feedback!")

def show_age_selector():
    st.subheader("Select your age group:")
    return st.selectbox("Age Group", ["6–12", "13–18", "19–25", "26+"])
