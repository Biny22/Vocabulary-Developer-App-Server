from pydantic import BaseModel
from typing import Dict, Optional


class WordBase(BaseModel):
    spelling: str
    type: str
    meanings: Dict[str, str]
    examples: Dict[str, str]


class WordRequest(BaseModel):
    word: WordBase
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
