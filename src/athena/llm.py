from ollama import chat

class LLMClient:
     """
     Wrapper around Ollama.

     Every future model (OpenAI, Gemini, Claude, local)
     should expose the same interface.
     """

     def __init__(self, model: str):
          self.model = model

     def generate(self, prompt: str) -> str:
            response = chat(
                  model = self.model,
                  messages =[
                        {
                              "role": "user",
                              "content": prompt
                        }
                  ]
            )
            return response["message"]["content"]