import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import pandas as pd
import gtts
from io import BytesIO

# Load or Create a CSV for responses
DATA_FILE = "responses.csv"
try:
    responses_df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    responses_df = pd.DataFrame(columns=["Question", "Response"])

# Predefined Questions
questions = [
    "What was the longest wait time you experienced this week when trying to get a manager's approval, and what was the specific situation?",
    "In the last three deals you worked, which CRM updates took you the most time to complete and why?",
    "What's one recurring customer question or concern that you find yourself addressing multiple times each day?",
    "During your last three Pre/Post Demo processes, which step caused the most delays or complications?",
    "What's one tool or resource you frequently need but have trouble accessing quickly during customer interactions?"
]

# UI Header
st.title("The Mirror - Employee Feedback")

# Select a Question
selected_question = st.selectbox("Select a Question", questions)

# Text Response Input
text_response = st.text_area("Your Response")

# Voice Input
st.write("Or record your response:")
r = sr.Recognizer()

def record_audio():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"

if st.button("Record Response"):
    text_response = record_audio()
    st.write("Recorded:", text_response)

# Save Response
if st.button("Submit Response"):
    new_entry = pd.DataFrame({"Question": [selected_question], "Response": [text_response]})
    responses_df = pd.concat([responses_df, new_entry], ignore_index=True)
    responses_df.to_csv(DATA_FILE, index=False)
    st.success("Response Saved!")

# Display Past Responses
st.subheader("Past Responses")
st.write(responses_df)
