from fastapi import FastAPI
from routers import router as media_router



app = FastAPI()
app.include_router(media_router)


