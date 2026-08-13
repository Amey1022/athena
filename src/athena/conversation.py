from athena.memory import MemoryManager
from athena.personality import SYSTEM_PROMPT
from athena.brain import Brain
from athena.semantic_memory import SemanticMemoryManager
from athena.models import Message
from athena.memory_detector import MemoryDetector

class ConversationManager:
    def __init__(self):
        print(">> Conversation Manager __init__ called")
        self.memory = MemoryManager()
        self.semantic_memory = SemanticMemoryManager()
        self.detector = MemoryDetector()
        if not self.memory.get_working_memory() or self.memory.get_working_memory()[0].role != "system":
            self.memory.initialize(SYSTEM_PROMPT)

    def chat(self, brain:Brain , user_message: str)->str:
        memories = self.detector.detect(user_message)
        for key, value in memories:
            self.semantic_memory.remember(key,value)
            print(f">> Learned semantic memory: {key} = {value} ")
        self.memory.add_message(
            "user",
            user_message
        )
        #build temporary context for the reasoning engine
        messages= list(self.memory.get_working_memory())
        semantic_context = self.semantic_memory.get_context()
        if semantic_context:
            messages.insert(
                1,
                Message(
                    role = "system",
                    content = semantic_context,
                ),
            ) 
        try:
            reply = brain.think(messages)
        except Exception as e:
            return f"Error communicating with reasoning engine: {e}"

        self.memory.add_message(
            "assistant",
            reply
        )
        return reply

    def shutdown(self)-> None:
        #Shut down conversation system
        self.memory.shutdown()
        self.semantic_memory.close()