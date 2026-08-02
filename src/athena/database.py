"""
SQLite database layer for ATHENA.

This module is responsible only for:
- Opening the SQLite database
- Creating tables
- Executing queries
- Closing the connection

Higher-level logic belongs in MemoryManager.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

class DatabaseManager:
    """Simple SQLite wrapper for ATHENA."""
    def __init__(self, db_path: str | Path = "data/database/athena.db"):
        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True) # ensuring data directory exists

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        #Create required tables if they do not already exist.
        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            summary TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS semantic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            updated_at TEXT NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT NOT NULL,
            importance REAL DEFAULT 0.5,
            tags TEXT,
            created_at TEXT NOT NULL
        );
        """)

        self.connection.commit()

    def execute (self, query: str, params: tuple = ())->sqlite3.Cursor:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetchall(self, query: str, params: tuple=())-> list[sqlite3.Row]:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query: str, params:tuple=())-> sqlite3.Row | None:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    
    def close(self)->None:
        self.connection.close()




