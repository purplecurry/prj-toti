<<<<<<< Updated upstream
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
import ai_service, my_calendar, db, timer, user, stats

=======
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db import engine, get_db 
import models
import my_calendar  # 1. 캘린더 파일 가져오기
>>>>>>> Stashed changes

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 여기에 캘린더 라우터를 등록합니다! (가장 중요)
app.include_router(my_calendar.router)

@app.get("/")
async def root():
<<<<<<< Updated upstream
    return RedirectResponse(url="/timer")
=======
    return {"message": "Tomato Project API is Running!"}

# 기존의 @app.post("/memo") 등 동제님 코드는 이 아래에 그대로 두시면 됩니다.
>>>>>>> Stashed changes
