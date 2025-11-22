import tempfile
import os
from functools import lru_cache
import shutil

# NOTE: do NOT import whisper at module import time; import lazily inside _load_model

@lru_cache(maxsize=1)
def _load_model(name: str = "tiny"):
    # lazy import so app won't crash at import time if whisper/ffmpeg missing
    try:
        import whisper
    except Exception as e:
        raise ImportError(
            "The 'openai-whisper' package failed to import. "
            "Install it with 'pip install -U openai-whisper'. "
            f"Underlying error: {e}"
        )

    if shutil.which("ffmpeg") is None:
        # raise to make Streamlit show a clear error instead of failing later with WinError 2
        raise FileNotFoundError(
            "ffmpeg not found on PATH. Install ffmpeg and add its 'bin' folder to your PATH. "
            "See https://ffmpeg.org/download.html"
        )

    print(f"DEBUG: Loading Whisper model '{name}' (this can take time)...")
    try:
        model = whisper.load_model(name)
        print("DEBUG: Whisper model loaded.")
        return model
    except Exception as e:
        print("ERROR: Failed to load Whisper model:", e)
        raise

def _save_uploaded_file_to_temp(uploaded_file):
    """
    Save a Streamlit UploadedFile to a temp file and return the filepath.
    """
    uploaded_file.seek(0)
    name = getattr(uploaded_file, "name", None) or "upload"
    _, ext = os.path.splitext(name)
    if not ext:
        ext = ".mp3"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    tmp.write(uploaded_file.read())
    tmp.flush()
    tmp.close()
    return tmp.name

def transcribe_audio(uploaded_file, model_name: str = "tiny"):
    """
    Transcribe a Streamlit UploadedFile (or a filepath string) using Whisper.
    Returns the transcription text or raises an exception on failure.
    """
    model = _load_model(model_name)

    # If user passed a path already, use it directly
    if isinstance(uploaded_file, str) and os.path.exists(uploaded_file):
        audio_path = uploaded_file
        cleanup = False
    else:
        audio_path = _save_uploaded_file_to_temp(uploaded_file)
        cleanup = True

    try:
        print(f"DEBUG: Starting transcription for {audio_path} ...")
        result = model.transcribe(audio_path)
        text = result.get("text", "").strip()
        print("DEBUG: Transcription finished.")
        return text
    except Exception as e:
        print("ERROR: Transcription failed:", e)
        raise
    finally:
        if cleanup and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception:
                pass
