# Backend - Text Adventure Game

## Features

- **AI-driven storytelling**: Uses OpenAI's API to generate dynamic game narratives.
- **FastAPI backend**: Manages game logic and user interactions.
- **SQLite database**: Stores user progress and game choices persistently.

## Tech Stack

- **FastAPI**: Efficient and high-performance API framework for Python.
- **OpenAI API**: Generates responses and narratives.
- **SQLite**: Lightweight database for storing game progress.

## Installation

### Prerequisites

- Python 3.9+
- SQLite3
- OpenAI API key

### Setup

1. Clone the repository:

   ```sh


   ```

2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```sh
   export OPENAI_API_KEY=your_openai_api_key
   ```
4. Run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

## API Endpoints

| Method | Endpoint | Description                             |
| ------ | -------- | --------------------------------------- |
| `POST` | `/play/` | Generates game text using OpenAI's API. |

## How It Works

1. The user starts a new game.
2. The backend interacts with OpenAI's API to generate responses based on user input.
3. The frontend displays the generated story and options for the next action.
4. The user's choices are saved in SQLite to maintain game state.

## Contributing

Feel free to submit issues and pull requests to enhance the game!

## License

MIT License
