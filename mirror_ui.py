import streamlit as st
import openai
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os

# Set OpenAI API key
OPENAI_API_KEY = "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"  

st.title("The Mirror AI Chat")

# User input box
user_input = st.text_input("Ask The Mirror:")

if st.button("Submit"):
    if user_input:
        # Get OpenAI response
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant."},
                      {"role": "user", "content": user_input}]
        )
        answer = response["choices"][0]["message"]["content"]
        
        # Display response
        st.write(answer)
        
        # Convert response to speech
        tts = gTTS(answer)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

# Voice Input
st.header("🎤 Speak to The Mirror")
r = sr.Recognizer()
with sr.Microphone() as source:
    if st.button("Start Listening"):
        st.write("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            spoken_text = r.recognize_google(audio)
            st.text(f"You said: {spoken_text}")
        except sr.UnknownValueError:
            st.write("Could not understand audio")
        except sr.RequestError:
            st.write("Error with voice recognition service")
