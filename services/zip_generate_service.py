from io import BytesIO
from zipfile import ZipFile

from schemas import Word


def create_zip(word: Word, front_image_file: BytesIO,
                audio_file: BytesIO = None) -> BytesIO:
    # back_image_file: BytesIO,
    zip_buf = BytesIO()
    with ZipFile(zip_buf, 'w') as zipf:
        zipf.writestr(f"{word.spelling}-front.png", front_image_file.getvalue())
        # zipf.writestr(f"{word.spelling}-back.png", front_image_file.getvalue())
        if audio_file:
            zipf.writestr(f"{word.spelling}-audio.mp3", audio_file.getvalue())
    zip_buf.seek(0)
    return zip_buf
