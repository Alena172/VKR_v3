from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.shared.database.session import get_session
from app.modules.vocabulary.application.services import VocabularyService
from app.modules.vocabulary.application.dto import WordCreateDTO, WordReadDTO
from app.modules.vocabulary.infrastructure.repository import VocabularyRepository
from app.modules.ai_engine.application.services import AIService

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


def get_vocabulary_service(
    session: AsyncSession = Depends(get_session),
) -> VocabularyService:
    repo = VocabularyRepository(session)
    ai = AIService()
    return VocabularyService(repo, ai)


@router.post("/", response_model=WordReadDTO)
async def add_word(
    user_id: UUID,  # временно query param, позже auth
    data: WordCreateDTO,
    service: VocabularyService = Depends(get_vocabulary_service),
):
    word = await service.add_word(user_id, data)
    return WordReadDTO(
        id=word.id,
        text=word.text,
        base_form=word.base_form,
        part_of_speech=word.part_of_speech,
        translations=[t.value for t in word.translations],
        difficulty=word.difficulty,
        created_at=word.created_at,
    )
