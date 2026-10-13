"""
Database schema definitions for RDRS.
All tables are created with SQLite.
"""

import sqlite3
import os


# Database path relative to this file
DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "rdrs.db"
)


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Create all tables if they don't exist.
    This is safe to run multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Events table: stores file activity
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            entropy REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Processes table: stores process information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER,
            name TEXT,
            cpu_percent REAL,
            memory_mb REAL,
            executable TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Alerts table: stores detected threats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            threat_score INTEGER,
            threat_level TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Incidents table: tracks alerts that need investigation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id INTEGER,
            status TEXT DEFAULT 'OPEN',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alert_id) REFERENCES alerts(id)
        )
    """)

    # Quarantine table: tracks quarantined files
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quarantine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_path TEXT NOT NULL,
            evidence_path TEXT NOT NULL,
            action_result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")
