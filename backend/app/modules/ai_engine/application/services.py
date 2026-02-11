from app.modules.ai_engine.infrastructure.translation import ContextualTranslator
from app.modules.ai_engine.infrastructure.sentence_generation import SentenceGenerator
from app.modules.ai_engine.infrastructure.difficulty import DifficultyEstimator


class AIService:
    def __init__(self):
        self.translator = ContextualTranslator()
        self.generator = SentenceGenerator()
        self.difficulty = DifficultyEstimator()

    async def translate_with_context(self, word: str, context: str):
        return await self.translator.translate(word, context)

    async def generate_sentence(self, word: str) -> str:
        return await self.generator.generate(word)

    async def estimate_difficulty(self, word: str, context_count: int) -> float:
        return await self.difficulty.estimate(word, context_count)

