from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.vocabulary.domain.models import Word, Context
from app.modules.vocabulary.domain.value_objects import Translation
from .orm import WordORM, TranslationORM, ContextORM


class VocabularyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, word: Word):
        orm_word = WordORM(
            id=word.id,
            user_id=word.user_id,
            text=word.text,
            base_form=word.base_form,
            part_of_speech=word.part_of_speech,
            difficulty=word.difficulty,
        )

        for t in word.translations:
            orm_word.translations.append(
                TranslationORM(id=uuid4(), value=t.value)
            )

        for c in word.contexts:
            orm_word.contexts.append(
                ContextORM(
                    id=c.id,
                    text=c.text,
                    source_url=c.source_url,
                )
            )

        self.session.add(orm_word)
        await self.session.commit()
