import sqlite3
import os
DB_URL = os.environ.get("DATABASE_URL")  # set on Render, empty locally
DB_PATH = os.path.join(os.path.dirname(__file__), "ecogacha.db")


def get_db():
    if DB_URL:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(DB_URL)
        conn.cursor_factory = psycopg2.extras.RealDictCursor
        return conn
    else:
        conn = sqlite3.connect("ecogacha.db")
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matric_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            tokens INTEGER DEFAULT 0,
            total_scans INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            waste_category TEXT NOT NULL,
            confidence REAL NOT NULL,
            tokens_earned INTEGER NOT NULL,
            gacha_tier TEXT NOT NULL,
            eco_tip TEXT,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS redemptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tokens_redeemed INTEGER NOT NULL,
            reward_id TEXT,
            reward_name TEXT,
            redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database initialised.")
