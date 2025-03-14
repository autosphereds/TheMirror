import streamlit as st
import speech_recognition as sr
import pandas as pd
import gtts
from io import BytesIO
import os

# Prewritten questions
questions = [
    "What was the longest wait time you experienced this week when trying to get a manager's approval, and what was the specific situation?",
    "In the last three deals you worked, which CRM updates took you the most time to complete and why?",
    "What's one recurring customer question or concern that you find yourself addressing multiple times each day?",
    "During your last three Pre/Post Demo processes, which step caused the most delays or complications?",
    "What's one tool or resource you frequently need but have trouble accessing quickly during customer interactions?"
]

# Load responses or create new file
csv_file = "responses.csv"
if os.path.exists(csv_file):
    responses_df = pd.read_csv(csv_file)
else:
    responses_df = pd.DataFrame(columns=["Question", "Response"])

st.title("📋 The Mirror: Employee Survey")

# Select a question
question_index = st.session_state.get("question_index", 0)
st.subheader(questions[question_index])

# Text input for response
text_response = st.text_area("Enter your response here:")

# Voice input
recognizer = sr.Recognizer()
if st.button("🎤 Record Response"):
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            voice_response = recognizer.recognize_google(audio)
            text_response = voice_response
            st.success("Voice response recorded!")
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results; check your internet connection.")

# Save response
if st.button("Submit Response") and text_response:
    new_entry = pd.DataFrame({"Question": [questions[question_index]], "Response": [text_response]})
    responses_df = pd.concat([responses_df, new_entry], ignore_index=True)
    responses_df.to_csv(csv_file, index=False)
    st.success("Response recorded!")

    # Move to next question
    if question_index < len(questions) - 1:
        st.session_state["question_index"] = question_index + 1
        st.experimental_rerun()
    else:
        st.success("All questions completed! Thank you.")

# Show responses (optional)
if st.checkbox("📊 View Responses"):
    st.dataframe(responses_df)
