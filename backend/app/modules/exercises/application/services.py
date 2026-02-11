from uuid import uuid4

from app.modules.exercises.domain.models import Exercise
from app.modules.exercises.domain.enums import ExerciseType
from app.modules.exercises.infrastructure.generators.fill_blank import FillBlankGenerator
from app.modules.exercises.infrastructure.generators.multiple_choice import MultipleChoiceGenerator
from app.modules.exercises.infrastructure.generators.translation import TranslationGenerator


class ExerciseService:
    def __init__(self):
        self.fill_blank = FillBlankGenerator()
        self.multiple_choice = MultipleChoiceGenerator()
        self.translation = TranslationGenerator()

    async def generate_fill_blank(self, user_id, word, context):
        question, answer = await self.fill_blank.generate(
            context.text, word.text
        )
        return Exercise(
            id=uuid4(),
            user_id=user_id,
            word_id=word.id,
            type=ExerciseType.FILL_BLANK,
            question=question,
            correct_answer=answer,
        )

    async def generate_multiple_choice(self, user_id, word):
        question, options, answer = await self.multiple_choice.generate(
            word.text,
            correct=word.translations[0].value,
            distractors=["идти", "делать", "смотреть"],
        )
        return Exercise(
            id=uuid4(),
            user_id=user_id,
            word_id=word.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question=question,
            options=options,
            correct_answer=answer,
        )
