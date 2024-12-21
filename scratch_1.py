import sounddevice as sd  # For real-time audio recording
import wave  # To save audio data in WAV format
import tempfile  # To create a temporary file for saving audio
import keyboard  # For detecting user key pressesrs
import numpy as np  # For handling audio data arrays

def record_audio_interactive(samplerate=16000):
    """
    Records audio interactively, starting and stopping based on user actions.

    Args:
        samplerate (int): Sample rate of the audio.

    Returns:
        str: Path to the saved WAV file.
    """
    print("Press 'r' to start recording and 's' to stop.")  # Instructions for the user

    try:
        audio_data = []  # List to store recorded audio chunks
        recording = False  # Flag to track whether recording is active

        while True:  # Infinite loop to continuously check for user actions
            if keyboard.is_pressed('r') and not recording:  # If 'r' is pressed and not already recording
                print("Recording started. Press 's' to stop.")  # Notify the user
                recording = True  # Set the recording flag to True
                audio_data = []  # Reset audio data list for a new recorsrding
                stream = sd.InputStream(samplerate=samplerate, channels=1, dtype="int16")  # Create audio stream
                stream.start()  # Start the audio stream

            if recording:  # If currently recording
                data, _ = stream.read(1024)  # Read audio in chunks of 1024 frames
                audio_data.append(data)  # Append the chunk to the audio data list

            if keyboard.is_pressed('s') and recording:  # If 's' is pressed and currently recording
                print("Recording stopped.")  # Notify the user
                recording = False  # Set the recording flag to False
                stream.stop()  # Stop the audio stream
                stream.close()  # Close the audio stream
                break  # Exit the loop

        # Combine recorded audio chunks into a single array
        audio_data = np.concatenate(audio_data)

        # Save the recorded audio to a temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")  # Create a temp file
        with wave.open(temp_file.name, 'w') as wav_file:  # Open the file for writing
            wav_file.setparams((1, 2, samplerate, 0, 'NONE', 'not compressed'))  # Set WAV file parameters
            wav_file.writeframes(audio_data.tobytes())  # Write audio data to the file

        print(f"Audio saved: {temp_file.name}")  # Notify the user of the file location
        return temp_file.name  # Return the file path

    except Exception as e:  # Catch and handle any errors
        print(f"Error: {e}")  # Print the error message
        return None  # Return None if an error occurs

# Example usage
if __name__ == "__main__":
    file_path = record_audio_interactive()  # Start the interactive recording function
    if file_path:  # If a file path is returned (successful recording)
        print(f"Audio file saved at: {file_path}")  # Notify the user of the saved file
    else:  # If no file path is returned (error occurred)
        print("Recording failed.")  # Notify the user of the failure

from groq import Groq

# Initialize the Groq client with your API key
client = Groq(api_key="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")  # Replace with your actual API key

def transcribe_audio():
    """Transcribes speech from an uploaded audio file using the Groq API."""

    #print("Upload your audio file...")
    #file_path = input("Enter the path to your audio file: ")

    try:
        # Open the audio file
        with open(file_path, "rb") as file:
            # Create a translation of the audio file
            translation = client.audio.translations.create(
                file=(file_path, file.read()),
                model="whisper-large-v3",  # Or another suitable model
                response_format="json",
            )

            # Print the translation text
            print(translation.text)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    transcribe_audio()
    print("tested2")


