import asyncio
from fastapi import APIRouter, Depends, Form
from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse
# from dependencies import verify_access_token

from services.image_generate_service import generate_image
from services.audio_generate_service import generate_audio
from services.zip_generate_service import create_zip
from core.executor import executor
from schemas import Word, WordRequest


# router = APIRouter()


# @router.post("/generate/media")
# def generate_media(
#     req: WordRequest
#     # user: dict = Depends(verify_access_token)
# ):
#     try:
#         word = req.word
#         audio_toggle = req.audio_toggle
#         resolution = req.resolution
#
#         # 이미지 두 장 생성(PIL)
#         image_files = generate_image(word, resolution)
#         # 오디오 파일 생성(TTS)
#         audio_file = generate_audio(word) if audio_toggle else None
#         zip_file = create_zip(word, image_files, audio_file)
#
#         return StreamingResponse(
#             iter([zip_file.getvalue()]),
#             media_type="application/zip",
#             headers={"Content-Disposition": f"attachment; filename={word.spelling}.zip"}
#         )
#
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": str(e)}
#         )

router = APIRouter()


@router.post("/generate/media")
async def generate_media(req: WordRequest):
    try:
        word = req.word
        resolution = req.resolution
        audio_toggle = req.audio_toggle

        loop = asyncio.get_running_loop()

        # 병렬 실행
        tasks = [loop.run_in_executor(executor, generate_image, word, resolution)]
        if audio_toggle:
            tasks.append(loop.run_in_executor(executor, generate_audio, word))

        results = await asyncio.gather(*tasks)

        image_files = results[0]
        audio_file = results[1] if audio_toggle else None

        # ZIP 파일 생성 (동기 처리)
        zip_file = create_zip(word, image_files, audio_file)

        return StreamingResponse(
            iter([zip_file.getvalue()]),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={word.spelling}.zip"
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
