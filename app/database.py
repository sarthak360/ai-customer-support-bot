import sqlite3
import uuid
from datetime import datetime

DB_NAME = "chat_sessions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            sender TEXT,
            message_text TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
        )
    ''')
    conn.commit()
    conn.close()

def create_new_session():
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_sessions (session_id) VALUES (?)", (session_id,))
    conn.commit()
    conn.close()
    return session_id

def add_message_to_session(session_id, sender, message_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_messages (session_id, sender, message_text) VALUES (?, ?, ?)",
        (session_id, sender, message_text)
    )
    conn.commit()
    conn.close()

def get_session_history(session_id, limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message_text FROM chat_messages WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
        (session_id, limit)
    )
    history = reversed(cursor.fetchall())
    conn.close()
    # Format for Ollama/LLM: 'role' and 'parts'/'content'
    return [{"role": "user" if sender == "user" else "model", "parts": [text]} for sender, text in history]