from schemas import Word

from io import BytesIO
from typing import List, Optional
from zipfile import ZipFile


def create_zip(word: Word, image_files: List[BytesIO],
               audio_file: Optional[BytesIO] = None) -> BytesIO:
    """
    단어 카드 앞/뒷면 이미지와 오디오를 zip으로 묶어 반환하는 함수
    """
    zip_buf = BytesIO()
    with ZipFile(zip_buf, 'w') as zipf:
        if len(image_files) > 0:
            zipf.writestr(f"{word.spelling}-front.png", image_files[0].getvalue())
        if len(image_files) > 1:
            zipf.writestr(f"{word.spelling}-back.png", image_files[1].getvalue())
        if audio_file:
            zipf.writestr(f"{word.spelling}-audio.mp3", audio_file.getvalue())

    zip_buf.seek(0)
    return zip_buf
