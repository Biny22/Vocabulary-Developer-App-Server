import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import media_router, template_download_router


app = FastAPI()
app.include_router(media_router)
app.include_router(template_download_router)



# ✅ 프론트엔드 도메인
origins = [
    "http://localhost:3000",  # React 개발 서버
]

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 허용할 Origin
    allow_credentials=True,
    allow_methods=["*"],        # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],        # 모든 요청 헤더 허용
)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    print(f"{request.url.path} took {process_time:.4f}s")
    return response


