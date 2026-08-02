from athena.memory import MemoryManager
from athena.personality import SYSTEM_PROMPT

class ConversationManager:
    def __init__(self):
        self.memory = MemoryManager()
        self.memory.add("system", SYSTEM_PROMPT)

    def chat(self, brain , user_message):
        self.memory.add(
            "user",
            user_message
        )
        reply = brain.think(self.memory.get_working_memory())

        self.memory.add(
            "assistant",
            reply
        )
        return reply