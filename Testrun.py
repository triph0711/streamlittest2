import streamlit as st
import sounddevice as sd
import wave
import tempfile
import numpy as np
from groq import Groq

# Initialize the Groq client with your API key
client = Groq(api_key="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")  # Replace with your actual API key

# --- Audio Capture Function ---
def record_audio_interactive(samplerate=16000):
    """
    Records audio and saves it as a temporary WAV file.
    """
    try:
        st.write("Recording... Please wait until it's completed.")
        audio_data = []  # To store chunks of audio data
        duration = st.slider("Select recording duration (seconds):", 1, 30, 5)

        # Record audio for the specified duration
        with sd.InputStream(samplerate=samplerate, channels=1, dtype="int16") as stream:
            for _ in range(0, int(samplerate / 1024 * duration)):
                data, _ = stream.read(1024)
                audio_data.append(data)

        # Combine chunks and save to temporary file
        audio_data = np.concatenate(audio_data)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp_file.name, 'w') as wav_file:
            wav_file.setparams((1, 2, samplerate, 0, 'NONE', 'not compressed'))
            wav_file.writeframes(audio_data.tobytes())

        return temp_file.name

    except Exception as e:
        st.write(f"Error during recording: {e}")
        return None

# --- Transcription Function ---
def transcribe_audio(audio_file_path):
    """
    Transcribes the audio file using the Groq API.
    """
    try:
        with open(audio_file_path, "rb") as file:
            translation = client.audio.translations.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3",
                response_format="json",
            )
        return translation.text

    except Exception as e:
        st.write(f"An error occurred during transcription: {e}")
        return None

# --- Streamlit UI ---
st.title("Speech-to-Text Application")
st.write("Record your voice and get the transcription.")

if st.button("Record and Transcribe"):
    st.info("Recording will begin shortly. Please wait...")
    file_path = record_audio_interactive()
    if file_path:
        st.success(f"Recording saved: {file_path}")
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(file_path)
            if transcript:
                st.subheader("Transcript:")
                st.write(transcript)
            else:
                st.error("Transcription failed.")
    else:
        st.error("Recording failed. Please try again.")
