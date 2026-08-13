from athena.memory import MemoryManager
from athena.personality import SYSTEM_PROMPT
from athena.brain import Brain
from athena.semantic_memory import SemanticMemoryManager
from athena.models import Message
from athena.memory_detector import MemoryDetector
from athena.episodic_memory import EpisodicMemoryManager

class ConversationManager:
    def __init__(self):
        print(">> Conversation Manager __init__ called")
        self.memory = MemoryManager()
        self.semantic_memory = SemanticMemoryManager()
        self.detector = MemoryDetector()
        self.episodic_memory = EpisodicMemoryManager()
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
        messages= list(self.memory.get_context_window(12))
        semantic_context = self.semantic_memory.get_context()
        if semantic_context:
            messages.insert(
                1,
                Message(
                    role = "system",
                    content = semantic_context,
                ),
            ) 
        print(f"Context size: {len(messages)} messages")
        try:
            reply = brain.think(messages)
        except Exception as e:
            return f"Error communicating with reasoning engine: {e}"

        self.memory.add_message(
            "assistant",
            reply
        )
        return reply

    def shutdown(self, brain: Brain)-> None:
        #Shut down conversation system
        messages = self.memory.get_working_memory()
        summary = brain.summarize(messages)
        self.episodic_memory.remember(
            summary=summary,
            importance= 0.8,
            tags= "conversation",
        )
        self.memory.shutdown(summary)
        self.semantic_memory.close()
        self.episodic_memory.close()