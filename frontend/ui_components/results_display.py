import streamlit as st

def display_result(transcription_text):
    if transcription_text:
        st.subheader("📝 Transcription Result")
        
        st.text_area(
            "Transcript",
            transcription_text,
            height=200,
        )
        
        st.download_button(
            label="Download transcription",
            data=transcription_text,
            file_name="transcription.txt",
            mime="text/plain"
        )
