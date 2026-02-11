from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime


class ContextCreateDTO(BaseModel):
    text: str
    source_url: Optional[str] = None


class WordCreateDTO(BaseModel):
    text: str
    base_form: str
    part_of_speech: str
    translations: List[str]
    context: Optional[ContextCreateDTO] = None


class WordReadDTO(BaseModel):
    id: UUID
    text: str
    base_form: str
    part_of_speech: str
    translations: List[str]
    difficulty: float
    created_at: datetime
