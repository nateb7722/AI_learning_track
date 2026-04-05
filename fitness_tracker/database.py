"""
Database layer for the fitness tracker.

Uses SQLite — a file-based database that ships with Python.
All data lives in a single .db file. No server needed.

This module handles:
- Creating tables (schema)
- Storing and retrieving users, meals, workouts, exercises, and sets
"""

import sqlite3
from datetime import datetime, date
from pathlib import Path

# Database file lives next to this script
DB_PATH = Path(__file__).parent / "fitness_tracker.db"


def get_connection() -> sqlite3.Connection:
    """
    Create a connection to the SQLite database.

    sqlite3.Row lets us access columns by name (row["protein"])
    instead of by index (row[3]), which makes code much more readable.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys — SQLite has them off by default.
    # This ensures we can't log a meal for a user that doesn't exist.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Create all tables if they don't already exist.

    'IF NOT EXISTS' means this is safe to call every time the app starts —
    it won't destroy existing data.
    """
    conn = get_connection()

    # ── Users ──────────────────────────────────────────────────────────
    # Each person who interacts with the bot gets a row here.
    # telegram_id is how we identify who sent a message.
    # Targets are nullable because during onboarding we ask for them
    # step by step — the row exists before targets are set.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id     INTEGER UNIQUE NOT NULL,
            name            TEXT,
            calorie_target  INTEGER,
            protein_target  INTEGER,
            carb_target     INTEGER,
            fat_target      INTEGER,
            workout_goals   TEXT,
            onboarding_done INTEGER DEFAULT 0,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Meals ──────────────────────────────────────────────────────────
    # One row per meal or snack logged. A user might log 4-6 times/day.
    # description stores the raw text ("chicken breast and rice")
    # so we can always go back and see what was originally said.
    # meal_type categorizes the entry (breakfast, lunch, dinner, snack,
    # pre_workout, post_workout). Useful for spotting patterns later
    # like "you're consistently low on protein at breakfast."
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            description TEXT NOT NULL,
            meal_type   TEXT,
            calories    REAL,
            protein     REAL,
            carbs       REAL,
            fat         REAL,
            logged_at   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ── Workouts ───────────────────────────────────────────────────────
    # Session-level data. One row per gym visit.
    # This is the top of a three-tier hierarchy:
    #   workout → exercises → sets
    # Aggregate info lives here: total duration, what muscle groups
    # were hit, how much was lifting vs cardio.
    # muscle_groups stores comma-separated values like "chest,shoulders,triceps"
    conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            description     TEXT,
            muscle_groups   TEXT,
            duration_mins   INTEGER,
            lifting_mins    INTEGER,
            cardio_mins     INTEGER,
            logged_at       TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ── Exercises ──────────────────────────────────────────────────────
    # Movement-level data within a workout. One row per exercise.
    # e.g., "Bench Press" — with summary stats across all sets.
    # total_sets and max_weight give a quick overview without
    # needing to query every individual set.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id      INTEGER NOT NULL,
            name            TEXT NOT NULL,
            total_sets      INTEGER,
            max_weight      REAL,
            notes           TEXT,
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        )
    """)

    # ── Sets ───────────────────────────────────────────────────────────
    # Rep-level data within an exercise. One row per set.
    # e.g., "Set 1: 8 reps @ 185 lbs"
    # This is the most granular level — lets us track progression
    # over time (are you adding reps or weight week to week?).
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sets (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id     INTEGER NOT NULL,
            workout_id      INTEGER NOT NULL,
            set_number      INTEGER NOT NULL,
            reps            INTEGER,
            weight          REAL,
            notes           TEXT,
            FOREIGN KEY (exercise_id) REFERENCES exercises(id),
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        )
    """)

    # ── Conversation History ───────────────────────────────────────────
    # Stores messages so Claude has context when responding.
    # role is either 'user' or 'assistant'.
    #
    # IMPORTANT: This table stores ALL messages, but we only send
    # a subset to Claude on each API call. The database is the real
    # memory — the context window is just a sliding window over it.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            role        TEXT NOT NULL,
            content     TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ── User functions ─────────────────────────────────────────────────────

def get_or_create_user(telegram_id: int) -> dict:
    """
    Look up a user by their Telegram ID. If they don't exist yet,
    create a new row (they just started chatting with the bot).

    Returns the user as a dictionary.
    """
    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()

    if user is None:
        conn.execute(
            "INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,)
        )
        conn.commit()
        user = conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()

    conn.close()
    return dict(user)


def update_user(telegram_id: int, **fields):
    """
    Update any fields on a user record.

    Uses **kwargs so we can call it flexibly:
        update_user(123, name="Nate", protein_target=180)

    The f-string for column names is safe here because the keys
    come from our own code, not user input. We parameterize the
    values to prevent SQL injection.
    """
    conn = get_connection()
    for key, value in fields.items():
        conn.execute(
            f"UPDATE users SET {key} = ? WHERE telegram_id = ?",
            (value, telegram_id)
        )
    conn.commit()
    conn.close()


# ── Meal functions ─────────────────────────────────────────────────────

def log_meal(user_id: int, description: str, calories: float,
             protein: float, carbs: float, fat: float,
             meal_type: str = None) -> dict:
    """Log a meal or snack and return the created record."""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO meals (user_id, description, meal_type, calories,
                              protein, carbs, fat)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, description, meal_type, calories, protein, carbs, fat)
    )
    meal = conn.execute(
        "SELECT * FROM meals WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.commit()
    conn.close()
    return dict(meal)


def get_meals_today(user_id: int) -> list[dict]:
    """Get all meals logged today for a user."""
    conn = get_connection()
    today = date.today().isoformat()
    meals = conn.execute(
        """SELECT * FROM meals
           WHERE user_id = ? AND date(logged_at) = ?
           ORDER BY logged_at""",
        (user_id, today)
    ).fetchall()
    conn.close()
    return [dict(m) for m in meals]


def get_daily_totals(user_id: int) -> dict:
    """
    Sum up today's macros for a user.

    COALESCE handles the case where no meals have been logged yet —
    instead of returning NULL, it returns 0.
    """
    conn = get_connection()
    today = date.today().isoformat()
    totals = conn.execute(
        """SELECT
               COALESCE(SUM(calories), 0) as calories,
               COALESCE(SUM(protein), 0) as protein,
               COALESCE(SUM(carbs), 0) as carbs,
               COALESCE(SUM(fat), 0) as fat,
               COUNT(*) as meal_count
           FROM meals
           WHERE user_id = ? AND date(logged_at) = ?""",
        (user_id, today)
    ).fetchone()
    conn.close()
    return dict(totals)


# ── Workout functions ──────────────────────────────────────────────────

def start_workout(user_id: int, description: str = None,
                  muscle_groups: str = None) -> dict:
    """
    Start a new workout session. Returns the workout record.
    Duration and other aggregate fields get filled in as exercises
    are logged or when the workout is finished.
    """
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO workouts (user_id, description, muscle_groups)
           VALUES (?, ?, ?)""",
        (user_id, description, muscle_groups)
    )
    workout = conn.execute(
        "SELECT * FROM workouts WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.commit()
    conn.close()
    return dict(workout)


def update_workout(workout_id: int, **fields):
    """Update fields on a workout (e.g., duration when finishing up)."""
    conn = get_connection()
    for key, value in fields.items():
        conn.execute(
            f"UPDATE workouts SET {key} = ? WHERE id = ?",
            (value, workout_id)
        )
    conn.commit()
    conn.close()


def get_active_workout(user_id: int) -> dict | None:
    """
    Find a workout from today that hasn't been given a duration yet.
    This is how we know someone is mid-workout — they started one
    but haven't finished it.
    """
    conn = get_connection()
    today = date.today().isoformat()
    workout = conn.execute(
        """SELECT * FROM workouts
           WHERE user_id = ? AND date(logged_at) = ?
                 AND duration_mins IS NULL
           ORDER BY logged_at DESC LIMIT 1""",
        (user_id, today)
    ).fetchone()
    conn.close()
    return dict(workout) if workout else None


def get_workouts_this_week(user_id: int) -> list[dict]:
    """
    Get all workouts from the last 7 days.

    Uses SQLite's date math: datetime('now', '-7 days') gives us
    the timestamp from exactly 7 days ago.
    """
    conn = get_connection()
    workouts = conn.execute(
        """SELECT * FROM workouts
           WHERE user_id = ? AND logged_at >= datetime('now', '-7 days')
           ORDER BY logged_at""",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(w) for w in workouts]


# ── Exercise functions ─────────────────────────────────────────────────

def add_exercise(workout_id: int, name: str, total_sets: int = None,
                 max_weight: float = None, notes: str = None) -> dict:
    """Add an exercise to a workout. Returns the created record."""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO exercises (workout_id, name, total_sets, max_weight, notes)
           VALUES (?, ?, ?, ?, ?)""",
        (workout_id, name, total_sets, max_weight, notes)
    )
    exercise = conn.execute(
        "SELECT * FROM exercises WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.commit()
    conn.close()
    return dict(exercise)


def get_exercises_for_workout(workout_id: int) -> list[dict]:
    """Get all exercises in a workout."""
    conn = get_connection()
    exercises = conn.execute(
        "SELECT * FROM exercises WHERE workout_id = ? ORDER BY id",
        (workout_id,)
    ).fetchall()
    conn.close()
    return [dict(e) for e in exercises]


# ── Set functions ──────────────────────────────────────────────────────

def add_set(exercise_id: int, workout_id: int, set_number: int,
            reps: int = None, weight: float = None,
            notes: str = None) -> dict:
    """Log a single set within an exercise. Returns the created record."""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO sets (exercise_id, workout_id, set_number,
                             reps, weight, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (exercise_id, workout_id, set_number, reps, weight, notes)
    )
    set_row = conn.execute(
        "SELECT * FROM sets WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.commit()
    conn.close()
    return dict(set_row)


def get_sets_for_exercise(exercise_id: int) -> list[dict]:
    """Get all sets for an exercise, ordered by set number."""
    conn = get_connection()
    sets = conn.execute(
        "SELECT * FROM sets WHERE exercise_id = ? ORDER BY set_number",
        (exercise_id,)
    ).fetchall()
    conn.close()
    return [dict(s) for s in sets]


# ── Conversation functions ─────────────────────────────────────────────

def save_message(user_id: int, role: str, content: str):
    """Save a message to conversation history."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO conversations (user_id, role, content)
           VALUES (?, ?, ?)""",
        (user_id, role, content)
    )
    conn.commit()
    conn.close()


def get_recent_messages(user_id: int, limit: int = 20) -> list[dict]:
    """
    Get the most recent messages for context.

    We limit to 20 messages to keep Claude's context window manageable
    and costs down. The subquery + ORDER BY trick gets the last N
    messages but returns them in chronological order.
    """
    conn = get_connection()
    messages = conn.execute(
        """SELECT role, content FROM (
               SELECT role, content, created_at FROM conversations
               WHERE user_id = ?
               ORDER BY created_at DESC
               LIMIT ?
           ) ORDER BY created_at ASC""",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(m) for m in messages]


# When this module is imported, make sure the tables exist.
# This runs once when the app starts.
init_db()
