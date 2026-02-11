from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.users.domain.models import User
from app.modules.users.infrastructure.orm import UserORM


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        orm_user = UserORM(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        self.session.add(orm_user)
        await self.session.commit()

    async def get_by_id(self, user_id):
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()

        if not orm_user:
            return None

        return User(
            id=orm_user.id,
            email=orm_user.email,
            is_active=orm_user.is_active,
            created_at=orm_user.created_at,
        )
