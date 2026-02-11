from datetime import datetime
from uuid import UUID, uuid4

from app.modules.ai_engine.application.services import AIService
from app.modules.vocabulary.application.dto import WordCreateDTO
from app.modules.vocabulary.domain.models import Context, Word
from app.modules.vocabulary.domain.value_objects import Translation
from app.modules.vocabulary.infrastructure.repository import VocabularyRepository


class VocabularyService:
    def __init__(self, repository: VocabularyRepository, ai_service: AIService):
        self.repository = repository
        self.ai = ai_service

    async def add_word(self, user_id: UUID, data: WordCreateDTO) -> Word:
        word = Word(
            id=uuid4(),
            user_id=user_id,
            text=data.text,
            base_form=data.base_form,
            part_of_speech=data.part_of_speech,
            translations=[],
        )

        if data.context:
            word.contexts.append(
                Context(
                    id=uuid4(),
                    text=data.context.text,
                    source_url=data.context.source_url,
                    created_at=datetime.utcnow(),
                )
            )

            translation = await self.ai.translate_with_context(
                data.text,
                data.context.text,
            )

            word.translations.append(Translation(value=translation.translation))

            word.difficulty = await self.ai.estimate_difficulty(
                data.text,
                context_count=1,
            )
        else:
            word.translations.extend(Translation(value=t) for t in data.translations)

        await self.repository.add(word)
        return word

    async def get_word(self, word_id: UUID) -> Word | None:
        return await self.repository.get_by_id(word_id)

    async def list_words(self, user_id: UUID) -> list[Word]:
        return await self.repository.list_by_user(user_id)
