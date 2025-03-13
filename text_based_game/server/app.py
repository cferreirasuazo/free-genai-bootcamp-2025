import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from config import OPENAI_API_KEY
from db import create_new_session, get_session_history, session_exists, save_game_entry

def read_prompt():
    with open('GamePrompt.txt') as f:
        lines = f.read()
        return lines


# Initialize FastAPI app
app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API setup
openai.api_key = OPENAI_API_KEY

# Request model for user input
class UserInput(BaseModel):
    session_id: str
    user_text: str

# Function to generate game response
def generate_game_response(history, user_message):

    prompt = str(read_prompt())
    user_history = ""
    for entry in history:
        user_history += f"Player: {entry['user_text']}\nGame: {entry['game_text']}\n"

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
                 + [{"role": "user", "content": user_message}],
    )
    return response.choices[0].message.content

@app.post("/start-session/")
async def start_session():
    session_id = create_new_session()
    return {"session_id": session_id}

@app.post("/play/")
async def play(input_data: UserInput):
    if not session_exists(input_data.session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID")

    # Retrieve session history
    history = get_session_history(input_data.session_id)
    print(history)
    game_text = generate_game_response(history, input_data.user_text)
    print(type(game_text))
    save_game_entry(input_data.session_id, input_data.user_text, game_text)
    return {
        "game_text": json.loads(game_text)
    }





