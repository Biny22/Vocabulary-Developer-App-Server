from io import BytesIO
from zipfile import ZipFile


def create_zip(word: str, front_image_file: BytesIO,
                audio_file: BytesIO = None) -> BytesIO:
    # back_image_file: BytesIO,
    zip_buf = BytesIO()
    with ZipFile(zip_buf, 'w') as zipf:
        zipf.writestr(f"{word}-front.png", front_image_file.getvalue())
        zipf.writestr(f"{word}-back.png", front_image_file.getvalue())
        if audio_file:
            zipf.writestr(f"{word}-audio.mp3", audio_file.getvalue())
    zip_buf.seek(0)
    return zip_buf
