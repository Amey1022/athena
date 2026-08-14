from athena.database import DatabaseManager
from athena.repository import MemoryRepository
from athena.semantic_memory import SemanticMemoryManager

def create_memory():
    database = DatabaseManager(":memory:")
    repository = MemoryRepository(database)

    return SemanticMemoryManager(repository)

def test_store_memory():
    memory = create_memory()
    memory.remember(
        "favourite_programming_language",
        "Python",
    )
    result = memory.recall(
        "favourite_programming_language"
    )
    assert result is not None
    assert result["value"] == "Python"

def test_update_memory():
    memory = create_memory()
    memory.remember(
        "favourite_programming_language",
        "Python"
    )
    memory.remember(
        "favourite_programming_language",
        "Rust",
    )
    result = memory.recall(
        "favourite_programming_language"
    )
    assert result is not None
    assert result["value"] == "Rust"

def test_delete_memory():
    memory = create_memory()
    memory.remember(
        "favourite_programming_language",
        "Python",
    )
    memory.forget(
        "favourite_programming_language"
    )
    assert(
        memory.recall(
            "favourite_programming_language"
        )
        is None
    )