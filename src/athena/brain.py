from typing import List
from athena.config import OLLAMA_MODEL
from athena.llm import LLMClient
from athena.models import Message

class Brain:

    def __init__ (self):
        self.llm = LLMClient(OLLAMA_MODEL)

    def think(self, messages: List[Message])-> str:
        return self.llm.generate(messages)

    def summarize(self, messages:List[Message]) -> str:
        """
        Generate a concise summary of the conversation.
        """
        prompt= [
            Message(
                role="system",
                content=(
                    "Summarize this conversation in 2-3 concise sentences. "
                    "Focus on what was accomplished and important decisions."
                ),
            )
        ]
        prompt.extend(messages)
        return self.llm.generate(prompt) 