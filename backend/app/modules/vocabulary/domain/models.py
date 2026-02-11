from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from .value_objects import Translation


@dataclass
class Context:
    id: UUID
    text: str
    source_url: Optional[str]
    created_at: datetime


@dataclass
class Word:
    id: UUID
    user_id: UUID
    text: str
    base_form: str
    part_of_speech: str
    translations: List[Translation] = field(default_factory=list)
    contexts: List[Context] = field(default_factory=list)
    difficulty: float = 0.5
    created_at: datetime = field(default_factory=datetime.utcnow)
