from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
# from core.security import verify_token  # JWT 검증 함수 (예시)
import os

from core import WORD_TEMPLATE_FILE


template_download_router = APIRouter()


@template_download_router.get("/download/word-template")
def download_word_template(
        # token: str = Depends(verify_token)
    ):
    """
    인증된 사용자만 템플릿 파일 다운로드 가능
    """
    print(f'file_dir: {WORD_TEMPLATE_FILE}')
    if not WORD_TEMPLATE_FILE.exists():
        raise HTTPException(status_code=404, detail="Template file not found")

    return FileResponse(
        path=WORD_TEMPLATE_FILE,
        filename="word template.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
