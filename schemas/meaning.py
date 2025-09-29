from pydantic import BaseModel

from schemas.part_of_speech import PartOfSpeech


class Meaning(BaseModel):
    definition: str
    part_of_speech: PartOfSpeech
