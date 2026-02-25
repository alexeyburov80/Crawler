import sqlite3
import os
from logs import logger

DB_DIR = "data"
DB_PATH = "data/database.db"

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dictionary (
            word TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_word ON dictionary(word)")

    conn.commit()
    conn.close()


def check_word(word: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM dictionary WHERE word LIKE ? LIMIT 5", (word + "%",))

    results = cursor.fetchall()
    conn.close()
    # return [row[0] for row in results]
    if len(results) == 0:
        logger.info(f"Not found in dictionary: {word}")