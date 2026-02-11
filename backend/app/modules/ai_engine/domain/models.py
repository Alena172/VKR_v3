from dataclasses import dataclass


@dataclass
class TranslationResult:
    word: str
    translation: str
    confidence: float


@dataclass
class DifficultyScore:
    value: float  # 0.0 – 1.0
