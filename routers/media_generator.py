from fastapi import APIRouter, Depends, Form
from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse

# from dependencies import verify_access_token

from services.image_generate_service import generate_front_card
from services.audio_generate_service import generate_audio
from services.zip_generate_service import create_zip
from schemas import Word, WordRequest


router = APIRouter()


@router.post("/generate/media")
def generate_media(
    req: WordRequest
    # user: dict = Depends(verify_access_token)
):
    try:
        word = req.word
        print(f'spelling: {word.spelling}')
        print(f'level: {word.level}')
        print(f'meanings: {word.meanings}')
        print(f'examples: {word.examples}')
        audio_toggle = req.audio_toggle
        resolution = req.resolution

        # print(f"wordType: {type(word.spelling)}")
        image_file = generate_front_card(word, resolution)
        print(f"이미지 생성 완료: {image_file}")
        audio_file = generate_audio(word) if audio_toggle else None
        print(f"오디오 생성 완료: {audio_file}")
        zip_file = create_zip(word, image_file, audio_file)

        return StreamingResponse(
            iter([zip_file.getvalue()]),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={word.spelling}.zip"}
        )

    except Exception as e:
        print(f'generate_media: {str(e)}')
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

        # return {"error": str(e)}
