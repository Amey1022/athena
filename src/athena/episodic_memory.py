from athena.repository import MemoryRepository

class EpisodicMemoryManager:
    """
    Manages ATHENA's episodic memory.

    Episodic memory stores important experiences,
    completed conversations, and significant events.
    """
    def __init__(self)-> None:
        print(">> Episodic Memory Manager __init__ called")
        self.repository = MemoryRepository()

    def remember(
            self,
            summary: str,
            importance: float = 0.5,
            tags: str = "",
    )-> None:
        self.repository.save_episode(
            summary = summary,
            importance = importance,
            tags = tags,
        )

    def recall_recent(self,limit: int = 5):
        return self.repository.get_recent_episodes(limit)

    def close(self)-> None:
        self.repository.close()

if __name__ == "__main__":

    memory = EpisodicMemoryManager()

    memory.remember(
        summary="Implemented automatic semantic memory in ATHENA.",
        importance=0.9,
        tags="athena,semantic-memory",
    )

    episodes = memory.recall_recent()

    for episode in episodes:
        print(dict(episode))

    memory.close()

    
if __name__ == "__main__":

    memory = EpisodicMemoryManager()

    print("\nRecent Episodes:\n")

    for episode in memory.recall_recent():
        print(dict(episode))

    memory.close()