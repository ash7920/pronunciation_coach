import streamlit as st
from backend.whisper_model import transcribe_audio
from backend.pronunciation_scoring import compare_text, score_pronunciation, generate_feedback
from frontend.ui_components.audio_upload import upload_audio_section
import streamlit.components.v1 as components


# -----------------------------
# CONFETTI THAT ALWAYS WORKS
# -----------------------------
def show_confetti():
    components.html(
        """
        <script>
        const parentDoc = window.parent.document;

        let canvas = parentDoc.getElementById("confetti-canvas");
        if (!canvas) {
            canvas = parentDoc.createElement("canvas");
            canvas.id = "confetti-canvas";
            canvas.style.position = "fixed";
            canvas.style.top = 0;
            canvas.style.left = 0;
            canvas.style.width = "100%";
            canvas.style.height = "100%";
            canvas.style.pointerEvents = "none";
            parentDoc.body.appendChild(canvas);
        }

        if (!parentDoc.confettiLoaded) {
            let script = parentDoc.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js";
            script.onload = () => { parentDoc.confettiLoaded = true; };
            parentDoc.head.appendChild(script);
        }

        setTimeout(() => {
            parentDoc.confetti({
                particleCount: 250,
                spread: 140,
                startVelocity: 45,
                origin: { y: 0.7 }
            });
        }, 300);
        </script>
        """,
        height=0,
        width=0
    )


# -----------------------------
# MAIN KIDS MODE FUNCTION
# -----------------------------
def run_kids_mode():

    st.title("🎈 Kids Mode – Fun Pronunciation Practice")

    st.markdown("### 👦 Choose a sentence to practice!")

    # ------------------------------------------------------
    # Choose a practice sentence (replace dropdown with a text input)
    # ------------------------------------------------------
    st.subheader("🎤 Say this sentence:")
    target_sentence = st.text_input(
        "Enter a sentence to practice:",
        value="The cat is drinking milk.",
        key="kids_target"
    )

    st.markdown("---")

    uploaded_file = upload_audio_section(key_prefix="kids_mode_uploader")

    if uploaded_file:
        with st.spinner("🎧 Listening carefully..."):
            text = transcribe_audio(uploaded_file)

        st.subheader("You said:")
        st.write(text)

        comparison = compare_text(target_sentence, text)
        score = score_pronunciation(comparison)
        feedback = generate_feedback(comparison)

        st.metric("Your Score 🎉", f"{score}%")
        st.write(feedback)

        if score >= 70:
            st.success("Great job! You did amazing! 🎉")
            st.balloons()
            show_confetti()
        else:
            st.warning("Keep practicing! You can do it! ⭐")
