from athena.database import DatabaseManager
from athena.models import Message

class MemoryRepository:
    """
    Handles persistence for ATHENA's memory.

    This class translates high-level memory operations into
    database operations.
    """
    def __init__(self):
        self.database = DatabaseManager()
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

    def close(self)-> None: 
        self.database.close()