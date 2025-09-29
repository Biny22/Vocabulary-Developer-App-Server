from enum import Enum


class WordLevel(str, Enum):
    ELEMENTARY = '초등'
    MIDDLE = '중등'
    HIGH = '고등'
    TOEIC = '토익'
    TOEFL = '토플'
