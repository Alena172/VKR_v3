from app.modules.ai_engine.domain.models import TranslationResult


class ContextualTranslator:
    async def translate(self, word: str, context: str) -> TranslationResult:
        # v1: простая эвристика
        if "company" in context.lower():
            translation = "управлять"
            confidence = 0.85
        else:
            translation = "бежать"
            confidence = 0.6

        return TranslationResult(
            word=word,
            translation=translation,
            confidence=confidence,
        )
