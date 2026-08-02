from typing import List
from athena.config import OLLAMA_MODEL
from athena.llm import LLMClient
from athena.models import Message

class Brain:

    def __init__ (self):
        self.llm = LLMClient(OLLAMA_MODEL)

    def think(self, messages: List[Message])-> str:
        return self.llm.generate(messages)