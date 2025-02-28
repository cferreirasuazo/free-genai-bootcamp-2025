import json
import streamlit as st
import requests
import pandas as pd
from config import BACKEND_IMPORTER_URL
from llmservice import llm_service

from json_reader import read_json
from utils import make_payload

st.title("Language Vocabulary Importer")

category = st.text_input("Enter a thematic category for vocabulary generation:")

def reset_table():
    st.session_state.vocabulary = None

if 'vocabulary' not in st.session_state:
    st.session_state.vocabulary = None

if st.button("Generate Vocabulary"):
    if category:
            # Generate vocabulary from OpenAI GPT API
        reset_table()
        # vocab_data = llm_service.generate_vocab(category)

        # # If data is successfully generated, store it
        # if not vocab_data:
        #     st.error("Failed to generate vocabulary. Please try again.")
        # llm_service.store_vocab_json(json.loads(vocab_data))
        
        words_response = read_json("vocab.json")
        group_name = list(words_response.keys())[0]
        words = words_response[group_name]
        st.session_state.category = category
        st.session_state.vocabulary = pd.DataFrame(words)
        st.session_state.words = words
        st.table(st.session_state.vocabulary)
        st.success("Vocabulary generated successfully!")
        
    else:
        st.warning("Please enter a thematic category.")

# Add a button to submit the generated vocabulary
if st.session_state.vocabulary is not None:
    if st.button("Submit Vocabulary"):
        # Make a request to another API endpoint to submit the vocabulary


        payload = {
            "group_name": st.session_state.category,
            "words": st.session_state.words
        }

        submit_response = requests.post(BACKEND_IMPORTER_URL, json=payload)
        if submit_response.status_code == 200:

            st.success(submit_response.json().get("message"))
        else:
            st.error("Failed to submit vocabulary. Please try again.")