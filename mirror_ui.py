import streamlit as st
import speech_recognition as sr

st.title("The Mirror - Employee Feedback")

questions = [
    "What was the longest wait time you experienced this week when trying to get a manager's approval, and what was the specific situation?",
    "In the last three deals you worked, which CRM updates took you the most time to complete and why?",
    "What's one recurring customer question or concern that you find yourself addressing multiple times each day?",
    "During your last three Pre/Post Demo processes, which step caused the most delays or complications?",
    "What's one tool or resource you frequently need but have trouble accessing quickly during customer interactions?",
]

question_index = st.session_state.get("question_index", 0)
st.write(f"**{questions[question_index]}**")

recognizer = sr.Recognizer()
mic = sr.Microphone()

def record_audio():
    with mic as source:
        st.write("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)  # Uses Google's free speech-to-text
        return text
    except sr.UnknownValueError:
        return "Speech not recognized."
    except sr.RequestError:
        return "Could not request results from Google Speech API."

if st.button("🎙️ Record Response"):
    text_response = record_audio()
    st.write("Recorded:", text_response)

if st.button("➡ Next Question"):
    if question_index < len(questions) - 1:
        st.session_state["question_index"] = question_index + 1
        st.experimental_rerun()
    else:
        st.write("✅ All questions have been answered. Thank you!")
