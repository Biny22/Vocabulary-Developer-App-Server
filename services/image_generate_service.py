import asyncio
from io import BytesIO
from typing import List
from fastapi import Form, HTTPException

from schemas import Word
from services.generate_front_card import generate_front_card
from services.generate_back_card import generate_back_card


def generate_image(word: Word, resolution: str = "4K", image_format='png'):
    if resolution == "HD":
        scale = 1
    elif resolution == "FHD":
        scale = 1.5
    else:
        scale = 2

    front_card = generate_front_card(word, scale, image_format)
    back_card = generate_back_card(word, scale, image_format)

    return [front_card, back_card]
