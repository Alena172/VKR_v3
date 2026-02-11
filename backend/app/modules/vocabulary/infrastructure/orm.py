from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.shared.database.base import Base


class WordORM(Base):
    __tablename__ = "words"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)

    text: Mapped[str] = mapped_column(String)
    base_form: Mapped[str] = mapped_column(String)
    part_of_speech: Mapped[str] = mapped_column(String)

    difficulty: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    translations = relationship("TranslationORM", back_populates="word")
    contexts = relationship("ContextORM", back_populates="word")


class TranslationORM(Base):
    __tablename__ = "translations"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    word_id: Mapped[UUID] = mapped_column(ForeignKey("words.id"))
    value: Mapped[str] = mapped_column(String)

    word = relationship("WordORM", back_populates="translations")


class ContextORM(Base):
    __tablename__ = "contexts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    word_id: Mapped[UUID] = mapped_column(ForeignKey("words.id"))
    text: Mapped[str] = mapped_column(String)
    source_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    word = relationship("WordORM", back_populates="contexts")
