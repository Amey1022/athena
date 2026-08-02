from typing import List, Dict

from athena.config import OLLAMA_MODEL
from athena.llm import LLMClient

class Brain:

    def __init__ (self):
        self.llm = LLMClient(OLLAMA_MODEL)

    def think(self, messages: List[Dict[str,str]])-> str:
        return self.llm.generate(messages)