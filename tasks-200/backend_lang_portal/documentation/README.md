# Language Learning Portal Backend

A FastAPI-based backend service for managing language learning, specifically designed for Japanese vocabulary study with support for kanji, romaji, and English translations.

## Features

- Word Management (kanji, romaji, English translations)
- Group Organization
- Study Sessions
- Review Tracking
- Activity Progress Monitoring

## Prerequisites

- Python 3.12 or higher
- SQLite3
- uv (Modern Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd backend-lang-portal
```

2. Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies:

```bash
uv pip install -r requirements.txt
```

5. Initialize the database:

```bash
uv run create_tables.py
```

## Running the Application

Start the development server:

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Words

- `GET /words` - List all words
- `GET /words/{word_id}` - Get specific word
- `POST /words` - Create new word
- `PUT /words/{word_id}` - Update word
- `DELETE /words/{word_id}` - Delete word

### Groups

- `GET /groups` - List all groups (paginated)
- `GET /groups/{group_id}` - Get specific group

### Study Sessions

- `POST /study_sessions` - Create new study session

## Data Models

### Word

```json
{
    "id": int,
    "kanji": str,
    "romaji": str,
    "english": str,
    "parts": dict
}
```

### Group

```json
{
    "id": int,
    "name": str,
    "words_count": int
}
```

### Study Session

```json
{
    "id": int,
    "group_id": int,
    "study_activity_id": int,
    "created_at": datetime
}
```

## Development

### Project Structure

```
backend-lang-portal/
├── main.py              # Application entry point
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── database.py          # Database configuration
├── repositories.py      # Data access layer
├── config.py           # Application configuration
└── routes/             # API endpoints
    ├── word_routes.py
    ├── groups_routes.py
    └── study_session_routes.py
```

### Database Management

The application uses SQLite as its database. The database file is created automatically when running `create_tables.py`.

### Adding New Features

1. Define models in `models.py`
2. Create schemas in `schemas.py`
3. Implement repository methods in `repositories.py`
4. Add routes in the appropriate route file under `routes/`

## Testing

To run tests:

```bash
uv run pytest
```

## Configuration

Configuration is managed through environment variables and the `.env` file:

```env
APP_NAME=FastAPI App
DEBUG=False
VERSION=1.0.0
API_PREFIX=/api/v1
DATABASE_URL=sqlite:///./sql_app.db
```

## API Documentation

Once the application is running, you can access:

- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`


## Run with Docker 

```
docker build -t backend-lang-portal .
docker run -d -p 8000:8000 backend-lang-portal  # run it in detached

```


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
