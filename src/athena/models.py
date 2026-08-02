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
