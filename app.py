import os
import streamlit as st

print("RUNNING FILE:", os.path.abspath(__file__))
from frontend.ui_components.audio_upload import upload_audio_section
from frontend.ui_components.results_display import display_result
from frontend.ui_components.kids_mode import run_kids_mode

# Try importing transcribe_audio safely
try:
    from backend.whisper_model import transcribe_audio
    from backend.pronunciation_scoring import compare_text, score_pronunciation, generate_feedback
    _import_error = None
except Exception as _e:
    transcribe_audio = None
    compare_text = None
    score_pronunciation = None
    generate_feedback = None
    _import_error = _e


st.set_page_config(
    page_title="AI Language Coach",
    page_icon="🎙️",
    layout="wide"
)

# Do NOT call upload_audio_section() here — remove any top-level uploader.
st.title("🎧 Your Speech Therapy Guide")

# --------------------
# Sidebar Mode Selector (combined)
# --------------------
# mode2 chooses between Normal UI (which contains Transcription/Exercise) and Kids Mode.
mode2 = st.sidebar.radio(
    "Kids Section",
    ["Normal Mode", "Kids Mode 🎈"]
)

if mode2 == "Kids Mode 🎈":
    # Render only the kids mode UI (it includes its own single uploader + heading)
    run_kids_mode()
else:
    # Normal Mode: show the main Transcription / Exercise options
    mode = st.sidebar.radio(
        "Choose Mode",
        ["Transcription", "Exercise Mode"]
    )
    print("DEBUG: CURRENT MODE =", mode)

    # ================================
    # MODE 1 — TRANSCRIPTION MODE
    # ================================
    if mode == "Transcription":

        uploaded_file = upload_audio_section(key_prefix="transcription_uploader")

        if uploaded_file:
            with st.spinner("Processing your audio..."):
                try:
                    # call the transcription backend
                    text = transcribe_audio(uploaded_file) if transcribe_audio is not None else None
                except Exception as e:
                    import traceback
                    st.error("Transcription failed — see details below.")
                    st.text(str(e))
                    st.text(traceback.format_exc())
                    text = None

            if text:
                # DEBUG: show raw transcription in the UI to verify Whisper output
                st.subheader("Raw transcription (debug)")
                st.text_area("transcription_raw", value=text, height=200)
                print("DEBUG: Transcribed text =", repr(text))

                # reuse the existing result display helper (if it shows sample, inspect that file)
                try:
                    display_result(text)
                except Exception as e:
                    st.warning("display_result failed; showing transcription only.")
                    st.write(text)


    # ================================
    # MODE 2 — EXERCISE MODE
    # ================================
    elif mode == "Exercise Mode":

        st.header("🗣 Repeat After Me Exercise")
        target_sentence = st.text_input(
            "Enter a sentence to practice:",
            "I would like a cup of tea."
        )

        uploaded_file = upload_audio_section(key_prefix="exercise_uploader")

        if uploaded_file:
            with st.spinner("Evaluating your pronunciation..."):
                try:
                    actual_text = transcribe_audio(uploaded_file) if transcribe_audio is not None else None
                except Exception as e:
                    import traceback
                    st.error("Failed to transcribe your exercise recording.")
                    st.text(str(e))
                    st.text(traceback.format_exc())
                    actual_text = None

            if actual_text:
                st.subheader("You said (transcription)")
                st.write(actual_text)

                # Compare and score
                if compare_text is not None:
                    comparison = compare_text(target_sentence, actual_text)
                    score = score_pronunciation(comparison) if score_pronunciation is not None else None
                    feedback = generate_feedback(comparison) if generate_feedback is not None else None

                    st.metric("Pronunciation score", f"{score}%" if score is not None else "N/A")
                    st.write("Feedback:")
                    st.write(feedback or "No feedback available.")
                else:
                    st.warning("Pronunciation scoring backend not available.")


# Debug log
print("DEBUG: Streamlit app finished rendering.")
