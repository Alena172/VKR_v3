from dataclasses import dataclass


@dataclass(frozen=True)
class Translation:
    value: str
    language: str = "ru"
