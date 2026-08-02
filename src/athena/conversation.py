from athena.memory import MemoryManager
from athena.personality import SYSTEM_PROMPT
from athena.brain import Brain

class ConversationManager:
    def __init__(self):
        self.memory = MemoryManager()
        self.memory.add_message("system", SYSTEM_PROMPT)

    def chat(self, brain:Brain , user_message: str)->str:
        self.memory.add_message(
            "user",
            user_message
        )
        reply = brain.think(self.memory.get_working_memory())

        self.memory.add_message(
            "assistant",
            reply
        )
        return reply