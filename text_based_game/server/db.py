import sqlite3
import uuid

DB_PATH = "text_adventure.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            session_id TEXT PRIMARY KEY
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_text TEXT,
            game_text TEXT,
            FOREIGN KEY (session_id) REFERENCES game_sessions(session_id)
        )
    """)
    conn.commit()
    conn.close()

# Generate a new session ID and save it
def create_new_session():
    session_id = str(uuid.uuid4())  # Generate unique session ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game_sessions (session_id) VALUES (?)", (session_id,))
    conn.commit()
    conn.close()
    return session_id

# Retrieve session history
def get_session_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_text, game_text FROM game_history WHERE session_id = ?", (session_id,))
    history = [{"user_text": row["user_text"], "game_text": row["game_text"]} for row in cursor.fetchall()]
    conn.close()
    return history

# Check if a session exists
def session_exists(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM game_sessions WHERE session_id = ?", (session_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Store user input and game response
def save_game_entry(session_id, user_text, game_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game_history (session_id, user_text, game_text) VALUES (?, ?, ?)",
                   (session_id, user_text, game_text))
    conn.commit()
    conn.close()

# Initialize database
init_db()
