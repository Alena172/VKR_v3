from dataclasses import dataclass
from uuid import UUID
from typing import List
from .enums import ExerciseType


@dataclass
class Exercise:
    id: UUID
    user_id: UUID
    word_id: UUID
    type: ExerciseType
    question: str
    correct_answer: str
    options: List[str] | None = None
