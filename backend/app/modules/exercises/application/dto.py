from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from app.modules.exercises.domain.enums import ExerciseType


class ExerciseReadDTO(BaseModel):
    id: UUID
    type: ExerciseType
    question: str
    options: Optional[List[str]]
