from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai_engine.application.services import AIService
from app.modules.vocabulary.application.dto import WordCreateDTO, WordReadDTO
from app.modules.vocabulary.application.services import VocabularyService
from app.modules.vocabulary.infrastructure.repository import VocabularyRepository
from app.shared.database.session import get_session

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


def get_vocabulary_service(
    session: AsyncSession = Depends(get_session),
) -> VocabularyService:
    repo = VocabularyRepository(session)
    ai = AIService()
    return VocabularyService(repo, ai)


def to_word_read_dto(word) -> WordReadDTO:
    return WordReadDTO(
        id=word.id,
        text=word.text,
        base_form=word.base_form,
        part_of_speech=word.part_of_speech,
        translations=[t.value for t in word.translations],
        difficulty=word.difficulty,
        created_at=word.created_at,
    )


@router.post("/", response_model=WordReadDTO)
async def add_word(
    user_id: UUID,  # временно query param, позже auth
    data: WordCreateDTO,
    service: VocabularyService = Depends(get_vocabulary_service),
):
    word = await service.add_word(user_id, data)
    return to_word_read_dto(word)


@router.get("/{word_id}", response_model=WordReadDTO)
async def get_word(
    user_id: UUID,
    word_id: UUID,
    service: VocabularyService = Depends(get_vocabulary_service),
):
    word = await service.get_word(word_id)

    if not word or word.user_id != user_id:
        raise HTTPException(status_code=404, detail="Word not found")

    return to_word_read_dto(word)


@router.get("/", response_model=list[WordReadDTO])
async def list_words(
    user_id: UUID,
    service: VocabularyService = Depends(get_vocabulary_service),
):
    words = await service.list_words(user_id)
    return [to_word_read_dto(word) for word in words]
