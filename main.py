import time
from fastapi import FastAPI, Request
from routers import router as media_router


app = FastAPI()
app.include_router(media_router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    print(f"{request.url.path} took {process_time:.4f}s")
    return response


