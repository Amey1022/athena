from athena.memory import MemoryManager
from athena.personality import SYSTEM_PROMPT
from athena.brain import Brain

class ConversationManager:
    def __init__(self):
        print(">> Conversation Manager __init__ called")
        self.memory = MemoryManager()
        if not self.memory.get_working_memory() or self.memory.get_working_memory()[0].role != "system":
            self.memory.initialize(SYSTEM_PROMPT)

    def chat(self, brain:Brain , user_message: str)->str:
        self.memory.add_message(
            "user",
            user_message
        )
        try:
            reply = brain.think(self.memory.get_working_memory())
        except Exception as e:
            return f"Error communicationg with reasoning engine: {e}"

        self.memory.add_message(
            "assistant",
            reply
        )
        return reply

    def shutdown(self)-> None:
        #Shut down conversation system
        self.memory.shutdown()