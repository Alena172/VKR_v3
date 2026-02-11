from uuid import uuid4
from datetime import datetime

from app.modules.vocabulary.domain.models import Word, Context
from app.modules.vocabulary.domain.value_objects import Translation
from app.modules.vocabulary.application.dto import WordCreateDTO
from app.modules.vocabulary.infrastructure.repository import VocabularyRepository


from app.modules.ai_engine.application.services import AIService


class VocabularyService:
    def __init__(self, repository, ai_service: AIService):
        self.repository = repository
        self.ai = ai_service

    async def add_word(self, user_id, data):
        word = Word(
            id=uuid4(),
            user_id=user_id,
            text=data.text,
            base_form=data.base_form,
            part_of_speech=data.part_of_speech,
            translations=[],
        )

        if data.context:
            translation = await self.ai.translate_with_context(
                data.text,
                data.context.text,
            )

            word.translations.append(
                Translation(value=translation.translation)
            )

            difficulty = await self.ai.estimate_difficulty(
                data.text,
                context_count=1,
            )
            word.difficulty = difficulty

        await self.repository.add(word)
        return word
