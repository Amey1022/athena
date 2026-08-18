from athena.memory import MemoryManager
from athena.personality import SYSTEM_PROMPT
from athena.brain import Brain
from athena.semantic_memory import SemanticMemoryManager
from athena.models import Message
from athena.memory_detector import MemoryDetector
from athena.episodic_memory import EpisodicMemoryManager
from athena.database import DatabaseManager
from athena.repository import MemoryRepository
from athena.logger import get_logger
from athena.nlp import NLPProcessor
from athena.importance import ImportanceScorer

logger = get_logger("Conversation")
class ConversationManager:
    def __init__(self):
        logger.info("ConversationManager initialized")
        database= DatabaseManager()
        repository = MemoryRepository(database)
        self.memory = MemoryManager(repository)
        self.semantic_memory = SemanticMemoryManager(repository)
        self.detector = MemoryDetector()
        self.episodic_memory = EpisodicMemoryManager(repository)
        self.nlp = NLPProcessor()
        self.importance = ImportanceScorer()
        if not self.memory.get_working_memory() or self.memory.get_working_memory()[0].role != "system":
            self.memory.initialize(SYSTEM_PROMPT)

    def chat(self, brain:Brain , user_message: str)->str:
        memories = self.detector.detect(user_message)
        for key, value in memories:
            self.semantic_memory.remember(key,value)
            logger.info(f"Learned semantic memory: {key}")
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
        summary = brain.summarize(messages) # Generate episodic memory
        features = self.nlp.extract_features(summary) # Extract NLP features
        importance = self.importance.score(features) # Calculate Importance
        tags = list(set(features.entities + features.lemmas[:3])) # Generate tags
        self.episodic_memory.remember(
            summary=summary,
            importance= importance,
            tags= tags,
        )
        self.memory.shutdown(summary)
        self.semantic_memory.close()
        self.episodic_memory.close()