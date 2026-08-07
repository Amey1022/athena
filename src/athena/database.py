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
from datetime import datetime 
from athena.models import Message

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

# ============================================================
# Sessions
# ============================================================ 
    def insert_session(self)-> int:
        #inserting new session and returning its id
        started_at = datetime.now().isoformat()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO sessions (started_at)
            VALUES (?)
            """,
            (started_at,)
        )
        self.connection.commit()
        if cursor.lastrowid is None:
             raise RuntimeError("Failed to create session!")

        return cursor.lastrowid

    def update_session(self, session_id: int, summary:str | None =None)-> None:
        #Update session when it ends
        ended_at = datetime.now().isoformat()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE sessions
            SET ended_at = ?, summary = ?
            WHERE id = ?
            """,
            (
                ended_at,
                summary,
                session_id,
            ),
        )
        self.connection.commit()

    def get_latest_session_id(self)-> int | None:
         cursor= self.connection.cursor()
         cursor.execute(
                  """
                    SELECT id
                    FROM sessions
                    WHERE ended_at IS NOT NULL
                    ORDER BY id DESC
                    LIMIT 1;
                  """
         )
         row = cursor.fetchone()
         if row is None:
              return None
         return int(row["id"])

    def get_conversation(self, session_id:int,)-> list[Message]:
         cursor= self.connection.cursor()
         cursor.execute(
               """
                SELECT
                    role,
                    content,
                    timestamp
                FROM conversations
                WHERE session_id = ?
                ORDER BY id ASC
                """,
                (session_id,),
         )
         rows =cursor.fetchall()
         return[
              Message(
                   role= row["role"],
                   content= row["content"],
                   timestamp=row["timestamp"],
              )
              for row in rows
         ]
    
# ============================================================
# Conversations
# ============================================================ 

    def insert_conversation(self, session_id:int, message:Message)-> None:
        #store a conversation message in the database
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO conversations (
                session_id,
                role,
                content,
                timestamp
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                session_id,
                message.role,
                message.content,
                message.timestamp,
            ),
        )
        self.connection.commit()
# ============================================================
# Semantic Memory
# ============================================================
    def save_semantic_memory(
              self,
              key: str, 
              value:str,
              confidence: float = 1.0,
    ) -> None:
         #Creates or updates semantic memory
         updated_at = datetime.now().isoformat()
         cursor = self.connection.cursor()
         cursor.execute(
              """
                INSERT INTO semantic_memory (
                    key,
                    value,
                    confidence,
                    updated_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key)
                DO UPDATE SET
                    value = excluded.value,
                    confidence = excluded.confidence,
                    updated_at = excluded.updated_at
                """,
            (
                 key,
                 value,
                 confidence,
                 updated_at,
            ),
         )
         self.connection.commit()

    def get_semantic_memory(self, key:str)-> sqlite3.Row | None:
         # Retrieve semantic memory by key
         cursor = self.connection.cursor()
         cursor.execute(
               """
                SELECT
                    id,
                    key,
                    value,
                    confidence,
                    updated_at
                FROM semantic_memory
                WHERE key = ?
                """,
                (key,), 
         )
         return cursor.fetchone()

    def get_all_semantic_memories(self)-> list[sqlite3.Row]:
         #Retrieves all semantic memories
         cursor= self.connection.cursor()
         cursor.execute(
                """
                SELECT
                    id,
                    key,
                    value,
                    confidence,
                    updated_at
                FROM semantic_memory
                ORDER BY updated_at DESC
                """
         )
         return cursor.fetchall()

    def delete_semantic_memory(self, key:str)-> None:
         #Delete a semanitc memory by key
         cursor = self.connection.cursor()
         cursor.execute(
              """
              DELETE FROM semantic_memory
              WHERE key = ?
              """,
             (key,),
         )
         self.connection.commit()
        
    def close(self)->None:
            self.connection.close()
                
    
    




