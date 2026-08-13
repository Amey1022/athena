import re

class MemoryDetector:
      """
    Detects simple, explicit facts in user messages.

    This is intentionally rule-based for ATHENA v0.2.
    It does not call an LLM.
    """
      def detect(self, message: str) -> list[tuple[str,str]]:
            memories = []

            match = re.search(
                  r"(?:my\s+)?favourite\s+programming\s+language\s+is\s+(.+?)(?:\.|$)",
                  message,
                  re.IGNORECASE
            )
            if match:
                  value = match.group(1).strip()

                  memories.append(
                       (
                        "favourite_programming_language",
                        value,
                       )
                  )
            return memories
if __name__ == "__main__":
    detector = MemoryDetector()

    test_messages = [
        "My favourite programming language is Python.",
        "My favourite programming language is C++",
        "I like Python.",
    ]

    for message in test_messages:
        print(f"\nMessage: {message}")

        memories = detector.detect(message)

        print(f"Detected: {memories}")