from ollama import chat

class LLMClient:

     def __init__(self, model: str):
          self.model = model

     def generate(self, messages):
            response = chat(
                  model = self.model,
                  messages = messages
            )
            
            return response["message"]["content"]