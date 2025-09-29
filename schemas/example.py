from typing import Optional
from pydantic import BaseModel

from .word_level import WordLevel


class Example(BaseModel):
    year: str
    month: Optional[str] = None
    level: WordLevel
    grade: Optional[str] = None
    exam_type: str
    sentence: str
