import random
import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas
from manga_ocr import MangaOcr
import torch

from api_client import get_words
from llm import get_random_sentence

torch.classes.__path__ = []  # Workaround for Streamlit and Torch issue

# Fetch Random Sentences from API
def fetch_random_text():
    try:
        words = get_words()
        random_number = random.randint(0, len(words) - 1)
        word = words[random_number]
        return get_random_sentence(word)
    except Exception as e:
        st.error(f"Error fetching text: {e}")
    return "こんにちは"

# Session State for Random Sentence
if "random_text" not in st.session_state:
    st.session_state["random_text"] = fetch_random_text()

st.title("Kana Practice App (MangaOCR)")

# Display Random Sentence
if st.button("Generate New Text"):
    st.session_state["random_text"] = fetch_random_text()

st.subheader(f"Write this: {st.session_state['random_text']}")

# Upload Image
uploaded_file = st.file_uploader("Upload an image of your handwritten text", type=["png", "jpg", "jpeg"])

# Drawing Canvas
st.subheader("Or draw the text here")
canvas_result = st_canvas(
    fill_color="#FFFFFF",
    stroke_width=8,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=200,
    width=400,
    drawing_mode="freedraw",
    key="canvas"
)

# Analyze Button
if st.button("Analyze Text"):
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
    elif canvas_result.image_data is not None:
        image_data = canvas_result.image_data
        if image_data is not None:
            image = Image.fromarray((image_data[:, :, :3] * 255).astype(np.uint8))
    
    if image:
        st.image(image, caption="Processed Image")
        
        with st.spinner("Analyzing text..."):
            mocr = MangaOcr()
            recognized_text = mocr(image)
        
        st.success(f"Recognized Text: {recognized_text}")
        
        # Validate with Generated Setence
        expected_text = st.session_state["random_text"]
        accuracy = 100 if recognized_text == expected_text else 0
        st.write(f"Accuracy: {accuracy}%")
        if accuracy == 100:
            st.success("Correct!")
        else:
            st.error("Try again!")
