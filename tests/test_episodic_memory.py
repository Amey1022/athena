from athena.database import DatabaseManager
from athena.repository import MemoryRepository
from athena.episodic_memory import EpisodicMemoryManager

def tes_store_episode():
    db = DatabaseManager(":memory:")
    repo = MemoryRepository(db)
    episodic = EpisodicMemoryManager(repo)

    episodic.remember(
        summary = "Implemented semantic memory architecture.",
        importance = 0.82,
        tags = ["athena", "memory"]
    )
    episodes =episodic.recall_recent()

    assert len(episodes) == 1
    assert episodes[0]["Importance"] == 0.82

def test_recent_order():
    db = DatabaseManager(":memory:")
    repo = MemoryRepository(db)
    episodic = EpisodicMemoryManager(repo)

    episodic.remember("First", 0.2, ["test"])
    episodic.remember("Second", 0.9, ["test"])

    episodes = episodic.recall_recent()

    assert episodes[0]["summary"] == "Second"