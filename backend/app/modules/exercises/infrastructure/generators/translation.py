class TranslationGenerator:
    async def generate(self, sentence: str, translation: str):
        question = f"Translate the sentence:\n{sentence}"
        return question, translation
