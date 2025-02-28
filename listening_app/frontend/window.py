import streamlit as st
import requests

from backend_client import get_video_questions
from utils import is_valid_youtube_url

# Backend URL (replace with actual backend endpoint)
BACKEND_URL = "http://your-backend-endpoint.com/process"

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state["history"] = []



st.title("Language Listening App")

# Sidebar to display URL submission history
st.sidebar.title("Submission History")
for entry in st.session_state["history"]:
    st.sidebar.write(f"🔗 {entry['url']}")
    st.sidebar.write(f"🎧 Selected: {entry['selected_answer']} ({'✅' if entry['correct'] else '❌'})")
    st.sidebar.write("---")

# User Input - URL
user_input_url = st.text_input("Enter a YouTube video URL:")

if st.button("Send"):
    if not user_input_url:
        st.warning("Please enter a valid URL.")
    elif not is_valid_youtube_url(user_input_url):
        st.error("❌ Invalid YouTube URL. Please enter a correct YouTube video link.")
    else:
        data = get_video_questions()

        if data:
            print(data)
            st.session_state["audio_url"] = data["audio_url"]
            st.session_state["options"] = data["options"]
            st.session_state["correct_answer"] = data["correct_answer"]
            st.session_state["selected_option"] = None
            st.session_state["feedback"] = None
            st.session_state["current_url"] = user_input_url
        else:
            st.error("Error fetching data from backend.")

# Check if data is available
if "audio_url" in st.session_state and st.session_state["audio_url"]:
    # Play the audio
    st.audio(st.session_state["audio_url"], format="audio/mp3")

    # Display options
    options = st.session_state["options"]
    selected_option = st.radio("Select your answer:", 
                               options=[opt["id"] for opt in options],
                               format_func=lambda x: next(opt["title"] for opt in options if opt["id"] == x))

    # Enable submit button only if an option is selected
    if selected_option:
        st.session_state["selected_option"] = selected_option

    if st.button("Submit", disabled=not st.session_state.get("selected_option")):
        is_correct = st.session_state["selected_option"] == st.session_state["correct_answer"]

        # Store the submission in history
        st.session_state["history"].append({
            "url": st.session_state["current_url"],
            "selected_answer": next(opt["title"] for opt in options if opt["id"] == st.session_state["selected_option"]),
            "correct": is_correct
        })

        # Show result feedback
        if is_correct:
            st.success("✅ Correct Answer!")
        else:
            st.error("❌ Wrong Answer! Try again.")
