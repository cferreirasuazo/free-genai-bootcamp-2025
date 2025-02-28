# Language Vocabulary Importer

A Streamlit application that helps generate and import Japanese vocabulary lists using AI assistance.

## Features

- Generate thematic vocabulary lists using AI
- View vocabulary in a structured table format
- Import vocabulary lists to a backend service
- Support for kanji, romaji, and English translations

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd vocab-importer
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your configuration:

```
BACKEND_IMPORTER_URL=<your-backend-url>
OPENAI_API_KEY=<your-openai-api-key>
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage

1. Enter a thematic category (e.g., "animals", "food", "weather")
2. Click "Generate Vocabulary" to create a new vocabulary list
3. Review the generated vocabulary in the table
4. Click "Submit Vocabulary" to send the list to the backend service

## Development

- The application uses Streamlit for the frontend interface
- OpenAI's GPT API is used for vocabulary generation
- Vocabulary is stored in JSON format with detailed word information
