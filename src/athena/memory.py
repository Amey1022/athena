from typing import List, Dict

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
        self.working_memory: List[Dict[str,str]] = []

    def add(self, role: str, content: str)-> None:
        self.working_memory.append(
            {
                "role": role,
                "content": content
            }
        )

    def get_working_memory(self)-> List[Dict[str,str]]:
        return self.working_memory
    def clear(self)-> None:
        self.working_memory.clear()
