class ImportanceScorer:
    """
    Scores how important a completed conversation is.
    Returns a value between 0.0 and 1.0.
    """
    HIGH_VALUE_KEYWORDS = [
        "implemented",
        "completed",
        "finished",
        "architecture",
        "refactor",
        "athena",
        "database",
        "memory",
        "vector",
        "project",
    ]
    LOW_VALUE_KEYWORDS = [
        "hello",
        "thanks",
        "thank you",
        "bye",
    ]

    def score(self, text: str)-> float:
        text = text.lower()

        score = 0.5
        for word in self.HIGH_VALUE_KEYWORDS:
            if word in text:
                score+=0.08

        for word in self.LOW_VALUE_KEYWORDS:
            if word in text:
                score-= 0.1

        return max(0.0,min(1.0,round(score,2)))