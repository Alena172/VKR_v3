from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.exercises.application.dto import ExerciseReadDTO
from app.modules.exercises.application.services import ExerciseService
from app.modules.vocabulary.infrastructure.repository import VocabularyRepository
from app.shared.database.session import get_session

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/fill-blank/{word_id}", response_model=ExerciseReadDTO)
async def generate_fill_blank(
    user_id: UUID,
    word_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    vocab_repo = VocabularyRepository(session)
    word = await vocab_repo.get_by_id(word_id)

    if not word or word.user_id != user_id:
        raise HTTPException(status_code=404, detail="Word not found")

    if not word.contexts:
        raise HTTPException(status_code=400, detail="No context available")

    service = ExerciseService()
    exercise = await service.generate_fill_blank(
        user_id=user_id,
        word=word,
        context=word.contexts[0],
    )

    return ExerciseReadDTO(
        id=exercise.id,
        type=exercise.type,
        question=exercise.question,
        options=exercise.options,
    )


@router.get("/multiple-choice/{word_id}", response_model=ExerciseReadDTO)
async def generate_multiple_choice(
    user_id: UUID,
    word_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    vocab_repo = VocabularyRepository(session)
    word = await vocab_repo.get_by_id(word_id)

    if not word or word.user_id != user_id:
        raise HTTPException(status_code=404, detail="Word not found")

    if not word.translations:
        raise HTTPException(status_code=400, detail="No translations available")

    service = ExerciseService()
    exercise = await service.generate_multiple_choice(user_id=user_id, word=word)

    return ExerciseReadDTO(
        id=exercise.id,
        type=exercise.type,
        question=exercise.question,
        options=exercise.options,
    )
