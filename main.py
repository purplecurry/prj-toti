from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
import models
from db import engine, get_db
import ai_service, my_calendar, db, timer, user, stats

# DB 테이블 생성 설정
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# CORS 설정 (프론트엔드 연동을 위해 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 캘린더 및 기타 라우터 등록
app.include_router(my_calendar.router)
# 다른 팀원들의 라우터도 필요하다면 여기에 추가 (예: app.include_router(timer.router))

# 2. 루트 경로 설정 (접속 시 타이머로 이동하거나 안내 메시지 출력)
@app.get("/")
async def root():
    # 타이머 페이지로 자동 이동시키려면 아래 주석을 해제하세요.
    # return RedirectResponse(url="/timer")
    return {"message": "Tomato Project API is Running!"}

# 기존의 @app.post("/memo") 등 DJ님 작업 코드가 이 아래에 있었다면 여기에 계속 작성하시면 됩니다.
