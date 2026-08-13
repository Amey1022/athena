from typing import List
from athena.models import Message
from athena.repository import MemoryRepository

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
        print(">> Memory Manager __init__ called")
        self.working_memory: List[Message] = []
        self.repository = MemoryRepository()
        self.current_session_id: int |None = None

    def initialize(self,system_prompt:str)-> None:
        self.restore_previous_session()
        self.working_memory.insert(
            0,
            Message(
                role="system",
                content= system_prompt,
            ),
        )
        self.start_session()

    def add_message(self, role: str, content: str)-> None:
        print(f"Saving message: {role}")
        message= Message(
            role = role,
            content = content,
        )
        self.working_memory.append(message)
        if self.current_session_id is not None:
            self.repository.save_message(
                self.current_session_id,
                message,
            )

    def start_session(self) ->None:
        # Start a new memory session
        self.current_session_id = self.repository.start_session()

    def end_session(self, summary:str | None = None)-> None:
        # End the current memory session
        if self.current_session_id is None:
            return
        self.repository.end_session(
            session_id=self.current_session_id,
            summary= summary,
        )
        self.current_session_id = None

    def get_working_memory(self)-> List[Message]:
        return self.working_memory

    def restore_previous_session(self)-> None:
        # restore most recent conversation into working memory
        previous= self.repository.load_latest_session()
        if previous:
            print(f"Restored {len(previous)} messages.")
        self.working_memory.extend(previous)

    def get_context_window(self, max_messages:int = 12)-> list[Message]:
        if len(self.working_memory)<= 1:
            return self.working_memory
        system = self.working_memory[0]
        recent = self.working_memory[-max_messages:]
        return [system] +  recent

    def clear(self)-> None:
        self.working_memory.clear()

    def shutdown(self, summary:str |None= None)-> None:
        #Gracefully shutdown the memory system
        self.end_session(summary)
        self.repository.close()
