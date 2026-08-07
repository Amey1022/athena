from athena.repository import MemoryRepository

class SemanticMemoryManager:
    """
    Manages ATHENA's long-term semantic memory.

    Semantic memory stores durable facts about the user,
    preferences, entities, and other information that should
    persist beyond an individual conversation.
    """
    def __init__(self) ->None:
      print(">> Semantic Memory Manager __init__ called")
      self.repository = MemoryRepository()

    def remember(
          self,
          key:str,
          value:str,
          confidence:float = 1.0,
    )-> None:
       # Store or update semantic memory
       self.repository.save_semantic_memory(
          key = key,
          value= value,
          confidence = confidence,
       )

    def recall(self,key:str):
       #Retrieve semantic memory by key
       return self.repository.get_semantic_memory(key)

    def recall_all(self):
       #Retrieves all semantic memories
       return self.repository.get_all_semantic_memories()

    def forget(self,key:str)-> None:
       #Delete a semantic memory
       self.repository.delete_semantic_memory(key)

    def close(self)-> None:
       #close this repository
       self.repository.close()

if __name__ == "__main__":
    memory = SemanticMemoryManager()
    # --------------------------------------------------------
    # 1. Store a memory
    # --------------------------------------------------------
    print("\n1. Storing memory...")

    memory.remember(
        "favourite_programming_language",
        "Python",
    )

    # --------------------------------------------------------
    # 2. Recall the memory
    # --------------------------------------------------------

    print("\n2. Recalling memory...")

    result = memory.recall("favourite_programming_language")

    print(dict(result) if result else "Memory not found")

    # --------------------------------------------------------
    # 3. Update the memory
    # --------------------------------------------------------

    print("\n3. Updating memory...")

    memory.remember(
        "favourite_programming_language",
        "C++",
        confidence=0.9,
    )

    result = memory.recall("favourite_programming_language")

    print(dict(result) if result else "Memory not found")

    # --------------------------------------------------------
    # 4. Forget the memory
    # --------------------------------------------------------

    print("\n4. Forgetting memory...")

    memory.forget("favourite_programming_language")

    # --------------------------------------------------------
    # 5. Verify deletion
    # --------------------------------------------------------

    print("\n5. Checking memory...")

    result = memory.recall("favourite_programming_language")

    print(dict(result) if result else "Memory not found")

    memory.close()