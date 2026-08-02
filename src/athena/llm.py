from typing import List 
from ollama import chat
from athena.models import Message

class LLMClient:

     def __init__(self, model: str):
          self.model = model

     def generate(self, messages: List[Message])-> str:
            ollama_messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]
            response = chat(
                  model = self.model,
                  messages = ollama_messages,
            )

            return response["message"]["content"]