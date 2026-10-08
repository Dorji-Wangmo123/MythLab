import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mythlab.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create all MythLab database tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    # ---------------- MYTHS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS myths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            image TEXT,
            region TEXT
        )
    """)

    # ---------------- CREATURES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS creatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            image TEXT,
            origin TEXT
        )
    """)

    # ---------------- REGIONS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image TEXT
        )
    """)

    # ---------------- QUIZ QUESTIONS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    # ---------------- FAVOURITES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_type TEXT NOT NULL,
            item_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    # ---------------- TASKS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("MythLab database created successfully!")