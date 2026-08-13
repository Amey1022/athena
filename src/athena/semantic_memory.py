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

    def get_context(self) -> str:
       #Return semantic memories formatted for llm context
       memories = self.recall_all()
       if not memories:
          return ""
       lines = ["Known facts about the user:"]
       for memory in memories:
          lines.append(
             f"-{memory['key']} : {memory['value']}"
          )
       return "\n".join(lines)
    def close(self)-> None:
       #close this repository
       self.repository.close()

