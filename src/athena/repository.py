from athena.database import DatabaseManager
from athena.models import Message

class MemoryRepository:
    """
    Handles persistence for ATHENA's memory.

    This class translates high-level memory operations into
    database operations.
    """
    def __init__(self,
                 database: DatabaseManager | None= None):
        self.database = database or DatabaseManager()
# ============================================================
# Sessions
# ============================================================

    def start_session(self)-> int:
        return self.database.insert_session()

    def end_session(self, session_id: int, summary:str |None =None)-> None:
        self.database.update_session(session_id= session_id, summary= summary,)
# ============================================================
# Conversations
# ============================================================

    def save_message(self, session_id:int, message: Message,)-> None:
        self.database.insert_conversation(session_id = session_id, message=message)

    def load_latest_session(self)-> list[Message]:
        # Load the most recent conversation from storage
        session_id= self.database.get_latest_session_id()
        print(f"loading session: {session_id}")
        if session_id is None:
            return[]
        messages= self.database.get_conversation(session_id)
        print(f"Loaded {len(messages)} messages")
        return messages
# ============================================================
# Semantic Memory
# ============================================================

    def save_semantic_memory(
            self,
            key:str,
            value:str,
            confidence: float = 1.0,
    ) -> None:
        #save or update semantic memory
        self.database.save_semantic_memory(
            key=key,
            value= value,
            confidence= confidence,
        )

    def get_semantic_memory(self, key:str):
        #Retrieve semantic memory by key
        return self.database.get_semantic_memory(key)

    def get_all_semantic_memories(self):
        #Retrieve all semantic memories
        return self.database.get_all_semantic_memories()

    def delete_semantic_memory(self, key:str)-> None:
        #Delete a semantic memory
        self.database.delete_semantic_memory(key)

# ============================================================
# Episodic Memory
# ============================================================
    def save_episode(
        self,
        summary: str,
        importance: float,
        tags: str,
    ) -> None:

        self.database.save_episode(
            summary=summary,
            importance=importance,
            tags=tags,
        )

    def get_recent_episodes(self, limit:int = 5):
        return self.database.get_recent_episodes(limit)

    def close(self)-> None: 
        self.database.close()

