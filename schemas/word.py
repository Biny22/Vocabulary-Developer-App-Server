from pydantic import BaseModel
from typing import Optional, List

from .word_level import WordLevel
from .meaning import Meaning
from .example import Example


class Word(BaseModel):
    spelling: str
    level: WordLevel
    meanings: List[Meaning]
    examples: List[Example]


class WordRequest(BaseModel):
    word: Word
    audio_toggle: bool = False
    resolution: str


# class WordCreate(WordBase):
#     """클라이언트 → 서버 (생성 요청)"""
#     pass
#
#
# class WordResponse(WordBase):
#     """DB → 클라이언트 (조회 응답)"""
#     image_url: Optional[str] = None
#     audio_url: Optional[str] = None
