import random


class MultipleChoiceGenerator:
    async def generate(self, word: str, correct: str, distractors: list[str]):
        options = distractors + [correct]
        random.shuffle(options)

        question = f"Choose the correct translation for '{word}'"
        return question, options, correct
