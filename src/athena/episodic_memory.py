from athena.repository import MemoryRepository
from athena.logger import get_logger
logger = get_logger("Episodic")

class EpisodicMemoryManager:
    """
    Manages ATHENA's episodic memory.

    Episodic memory stores important experiences,
    completed conversations, and significant events.
    """
    def __init__(self,
                 repository: MemoryRepository,)-> None:
        logger.info("EpisodicMemoryManager initialized")
        self.repository = repository

    def remember(
            self,
            summary: str,
            importance: float ,
            tags: list[str],
    )-> None:
        self.repository.save_episode(
            summary = summary,
            importance = importance,
            tags = tags
        )

    def recall_recent(self,limit: int = 5):
        return self.repository.get_recent_episodes(limit)

    def close(self)-> None:
        self.repository.close()


