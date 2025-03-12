import streamlit as st
import openai
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import gtts
from io import BytesIO
import tempfile
import os

# Set OpenAI API Key (Replace 'your-api-key' with your actual key)
openai.api_key = "your-api-key"

# Streamlit App Title
st.title("🤖 The Mirror - AI-Powered Consultant")

# User input section
st.subheader("💬 Type your question:")
user_input = st.text_area("Ask The Mirror...", height=150)

# OpenAI GPT Response Function
def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-4 if available
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Voice Input Section
st.subheader("🎤 Speak to The Mirror")
recognizer = sr.Recognizer()

def record_audio(duration=5, samplerate=16000):
    st.write("🎙 Listening...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()
    return np.squeeze(recording)

def recognize_audio():
    with st.spinner("Processing audio..."):
        audio_data = record_audio()
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "❌ Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"❌ Error connecting to Google API: {e}"

# Buttons for text & voice input
if st.button("🔍 Get AI Response"):
    if user_input.strip():
        response = get_openai_response(user_input)
        st.subheader("💡 The Mirror's Response:")
        st.write(response)
    else:
        st.warning("Please enter a question!")

if st.button("🎙 Start Voice Input"):
    voice_text = recognize_audio()
    st.write(f"🗣 You said: {voice_text}")
    if "❌" not in voice_text:
        response = get_openai_response(voice_text)
        st.subheader("💡 The Mirror's Response:")
        st.write(response)

# Text-to-Speech Output
st.subheader("🔊 Hear the Response")
if st.button("🔈 Play Response"):
    if user_input.strip():
        response_text = get_openai_response(user_input)
        tts = gtts.gTTS(response_text)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")
        os.remove(temp_file.name)
    else:
        st.warning("Enter a question first!")

# Footer
st.markdown("**🚀 Powered by The Mirror AI**")
