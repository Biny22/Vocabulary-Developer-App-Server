from gtts import gTTS
from io import BytesIO
import locale

from schemas import WordBase


def generate_audio(word: WordBase) -> BytesIO:
    # spelling = word.spelling.lower()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    spelling = "apple"
    buf = BytesIO()
    tts = gTTS(text=spelling, lang="en")
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf
