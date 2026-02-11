class FillBlankGenerator:
    async def generate(self, sentence: str, word: str):
        question = sentence.replace(word, "_____")
        return question, word
