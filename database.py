import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "gaming_radar_demo.db"

def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                url TEXT PRIMARY KEY,
                subreddit TEXT NOT NULL,
                title TEXT NOT NULL,
                score INTEGER,
                comments INTEGER,
                created TEXT NOT NULL
            )
        """)

def save_posts(rows):
    initialize_database()

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            INSERT INTO posts
            (url, subreddit, title, score, comments, created)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                score = excluded.score,
                comments = excluded.comments
        """, [
            (
                row["url"],
                row["subreddit"],
                row["title"],
                row["score"],
                row["comments"],
                row["created"]
            )
            for row in rows
        ])

def load_posts():
    initialize_database()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY created DESC"
        ).fetchall()

    return [dict(row) for row in rows]

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
    print(f"Database location: {DB_PATH}")
    print(f"Stored posts: {len(load_posts())}")