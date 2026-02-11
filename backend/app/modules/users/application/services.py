from uuid import uuid4
from datetime import datetime

from app.modules.users.domain.models import User
from app.modules.users.application.dto import UserCreateDTO
from app.modules.users.infrastructure.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, data: UserCreateDTO) -> User:
        user = User(
            id=uuid4(),
            email=data.email,
            is_active=True,
            created_at=datetime.utcnow(),
        )
        await self.repository.add(user)
        return user

    async def get_user(self, user_id):
        return await self.repository.get_by_id(user_id)
