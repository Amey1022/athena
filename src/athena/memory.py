from typing import List
from athena.database import DatabaseManager
from athena.models import Message

class MemoryManager:
    """
    Manages ATHENA's memory.

    For now this only stores the current conversation.
    Later it will also manage:
        - Episodic Memory
        - Semantic Memory
        - Knowledge Base
    """

    def __init__ (self) -> None:
        self.working_memory: List[Message] = []
        self.database = DatabaseManager()
        self.current_session_id: int |None = None
        self.start_session()

    def add_message(self, role: str, content: str)-> None:
        message= Message(
            role = role,
            content = content,
        )
        self.working_memory.append(message)
        if self.current_session_id is not None:
            self.database.insert_conversation(
                self.current_session_id,
                message = message,
            )

    def start_session(self) ->None:
        # Start a new memory session
        self.current_session_id = self.database.insert_session()

    def end_session(self, summary:str | None = None)-> None:
        # End the current memory session
        if self.current_session_id is None:
            return
        self.database.update_session(
            session_id=self.current_session_id,
            summary= summary,
        )
        self.current_session_id = None

    def get_working_memory(self)-> List[Message]:
        return self.working_memory
    def clear(self)-> None:
        self.working_memory.clear()

    def shutdown(self, summary:str |None= None)-> None:
        #Gracefully shutdown the memory system
        self.end_session(summary)
        self.database.close()
