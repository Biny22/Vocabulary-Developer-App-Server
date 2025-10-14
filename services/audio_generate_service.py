from gtts import gTTS
from io import BytesIO
from starlette.responses import JSONResponse
import locale

from schemas import Word


def generate_audio(word: Word) -> JSONResponse:
    spelling = word.spelling.lower()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    buf = BytesIO()
    tts = gTTS(text=spelling, lang="en")
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf
