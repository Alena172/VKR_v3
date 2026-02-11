from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_session
from app.modules.users.application.services import UserService
from app.modules.users.application.dto import UserCreateDTO, UserReadDTO
from app.modules.users.infrastructure.repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


@router.post("/", response_model=UserReadDTO)
async def create_user(
    data: UserCreateDTO,
    service: UserService = Depends(get_user_service),
):
    user = await service.create_user(data)
    return user


@router.get("/{user_id}", response_model=UserReadDTO)
async def get_user(
    user_id,
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
