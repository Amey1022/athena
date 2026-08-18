from typing import List
from athena.config import OLLAMA_MODEL
from athena.llm import LLMClient
from athena.models import Message

class Brain:

    def __init__ (self):
        self.llm = LLMClient(OLLAMA_MODEL)

    def think(self, messages: List[Message])-> str:
        return self.llm.generate(messages)

    def _conversation_to_text(self, messages: List[Message])-> str:
        return "\n".join(
            f"{m.role}: {m.content}"
            for m in messages
            if m.role != "system"
        )

    def summarize(self, messages:List[Message]) -> str:
        """
        Generate a concise summary of the conversation.
        """
        transcript = self._conversation_to_text(messages)

        prompt= [
            Message(
                role="system",
                content=(
                    "You are generating an episodic memory for an AI assistant.\n"
                    "Write a 2-3 sentence factual summary.\n"
                    "Focus only on accomplishments, decisions, technical progress, "
                    "and important outcomes. Do not include greetings or small talk."
                ),
            ), 
            Message(
                role = "user",
                content=transcript,
            ),
        ]

        return self.llm.generate(prompt) 