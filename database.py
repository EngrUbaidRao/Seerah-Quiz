"""
database.py
Handles all SQLite operations for the Seerah Quiz app:
- storing each quiz attempt
- fetching leaderboard (top scores)
- fetching a player's personal history
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "quiz_data.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the results table if it doesn't already exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            player_email TEXT,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            time_taken_seconds INTEGER,
            played_at TEXT NOT NULL
        )
        """
    )
    # Lightweight migration in case an older db file (without player_email) already exists
    existing_cols = [row["name"] for row in conn.execute("PRAGMA table_info(quiz_results)")]
    if "player_email" not in existing_cols:
        conn.execute("ALTER TABLE quiz_results ADD COLUMN player_email TEXT")
    conn.commit()
    conn.close()


def save_result(player_name: str, player_email: str, score: int, total_questions: int, time_taken_seconds: int | None = None):
    """Insert a completed quiz attempt into the database."""
    percentage = round((score / total_questions) * 100, 2)
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO quiz_results (player_name, player_email, score, total_questions, percentage, time_taken_seconds, played_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            player_name.strip(),
            player_email.strip(),
            score,
            total_questions,
            percentage,
            time_taken_seconds,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()


def get_leaderboard(limit: int = 10):
    """Return the top N results ordered by percentage (desc), then most recent."""
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT player_name, score, total_questions, percentage, played_at
        FROM quiz_results
        ORDER BY percentage DESC, played_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return rows


def get_player_history(player_name: str, limit: int = 5):
    """Return a specific player's most recent attempts."""
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT score, total_questions, percentage, played_at
        FROM quiz_results
        WHERE player_name = ?
        ORDER BY played_at DESC
        LIMIT ?
        """,
        (player_name.strip(), limit),
    ).fetchall()
    conn.close()
    return rows


def get_total_attempts():
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) as c FROM quiz_results").fetchone()["c"]
    conn.close()
    return count
