from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
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

    async def get_by_id(self, word_id):
        stmt = (
            select(WordORM)
            .where(WordORM.id == word_id)
            .options(
                selectinload(WordORM.translations),
                selectinload(WordORM.contexts),
            )
        )
        result = await self.session.execute(stmt)
        orm_word = result.scalar_one_or_none()

        if not orm_word:
            return None

        return Word(
            id=orm_word.id,
            user_id=orm_word.user_id,
            text=orm_word.text,
            base_form=orm_word.base_form,
            part_of_speech=orm_word.part_of_speech,
            translations=[Translation(value=t.value) for t in orm_word.translations],
            contexts=[
                Context(
                    id=c.id,
                    text=c.text,
                    source_url=c.source_url,
                    created_at=c.created_at,
                )
                for c in orm_word.contexts
            ],
            difficulty=orm_word.difficulty,
            created_at=orm_word.created_at,
        )

    async def list_by_user(self, user_id):
        stmt = (
            select(WordORM)
            .where(WordORM.user_id == user_id)
            .options(
                selectinload(WordORM.translations),
                selectinload(WordORM.contexts),
            )
        )
        result = await self.session.execute(stmt)
        words = result.scalars().all()

        return [
            Word(
                id=orm_word.id,
                user_id=orm_word.user_id,
                text=orm_word.text,
                base_form=orm_word.base_form,
                part_of_speech=orm_word.part_of_speech,
                translations=[Translation(value=t.value) for t in orm_word.translations],
                contexts=[
                    Context(
                        id=c.id,
                        text=c.text,
                        source_url=c.source_url,
                        created_at=c.created_at,
                    )
                    for c in orm_word.contexts
                ],
                difficulty=orm_word.difficulty,
                created_at=orm_word.created_at,
            )
            for orm_word in words
        ]
