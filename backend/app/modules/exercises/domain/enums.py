from enum import Enum


class ExerciseType(str, Enum):
    FILL_BLANK = "fill_blank"
    MULTIPLE_CHOICE = "multiple_choice"
    TRANSLATION = "translation"
