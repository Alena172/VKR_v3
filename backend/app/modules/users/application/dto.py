from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreateDTO(BaseModel):
    email: EmailStr


class UserReadDTO(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
