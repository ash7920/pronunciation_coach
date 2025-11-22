import streamlit as st

print("DEBUG: upload_audio_section() LOADED")


def upload_audio_section(key_prefix: str = "main"):
    """
    Upload/record audio UI. Use key_prefix to avoid duplicate Streamlit keys.
    """
    # Example unique keys for each widget
    uploaded_file = st.file_uploader(
        "Upload audio file",
        type=["mp3", "wav", "m4a"],
        key=f"{key_prefix}_file_uploader"
    )
    # If you render an audio player or other widgets, give them unique keys too:
    if uploaded_file:
        # st.audio doesn't accept a `key` argument — remove it.
        # If you need a keyed wrapper, use a container/placeholder with a key:
        with st.container():  # optional: st.container(key=f"{key_prefix}_container")
            st.audio(uploaded_file, format="audio/wav", start_time=0)

    # ...other UI widgets should use keys like f"{key_prefix}_something"
    return uploaded_file

print("DEBUG: uploader rendered")
