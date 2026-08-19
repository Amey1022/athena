"""
Domain models used throughout ATHENA.
"""

from dataclasses import dataclass, field
from datetime import datetime

@dataclass(slots=True)
class Message:
    #Represents single message in a conversation
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass(slots=True)
class NLPFeatures:
    token_count:int
    sentence_count:int

    noun_ratio:float
    verb_ratio:float

    entity_count:int
    entities: list[str]

    lemmas: list[str]

@dataclass(slots=True)
class SemanticFact:
    category: str
    key: str
    value: str
    confidence: float = 1.0

