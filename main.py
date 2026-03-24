from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager  # <-- 이게 빠지면 에러가 납니다!

# 1. 먼저 app 객체를 생성합니다.
app = FastAPI()

# 2. CORS 보안 설정을 바로 아래에 추가합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import ai_service, my_calendar, db, timer, user, stats


@asynccontextmanager
async def app_life_span(app: FastAPI):
    # 비동기 엔진으로 테이블을 생성하는 올바른 방법입니다
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=app_life_span)

# app = FastAPI() 바로 밑에 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 곳에서 접속 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(timer.router)
app.include_router(my_calendar.router)
app.include_router(ai_service.router)
app.include_router(user.router)
app.include_router(stats.router)
app.include_router(stats.stats_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/timer")

# main.py 혹은 해당 라우터 파일에 추가
from fastapi import APIRouter

# 만약 이미 router 객체가 있다면 그걸 사용하세요!
@app.post("/memo")
async def create_memo(title: str, content: str, date: str):
    # 여기서 DB에 저장하는 로직이 들어가면 됩니다.
    # 일단은 잘 받았는지 확인용으로 로그만 찍어볼게요!
    print(f"메모 수신: 날짜={date}, 제목={title}, 내용={content}")
    return {"status": "success", "message": "메모가 서버에 저장되었습니다!"}

@app.get("/memo/{date}")
async def get_memo(date: str):
    # 실제로는 여기서 DB를 조회해야 합니다. 
    # 지금은 테스트를 위해 가짜 데이터를 돌려주는 코드를 짜 드릴게요!
    
    print(f"{date} 날짜의 메모 조회 요청이 들어왔습니다.")
    
    # 예시: DB에서 해당 날짜 메모를 찾았다고 가정
    # 만약 DB 연결 전이라면 아래처럼 응답을 보내 테스트해보세요.
    return {
        "date": date,
        "title": "오늘의 학습 주제",
        "content": "여기에 저장된 메모 내용이 나타납니다!"
    }

# main.py에 추가
@app.get("/memo/{date}")
async def get_memo(date: str):
    # 지금은 테스트용으로 가짜 데이터를 보내줄게요.
    # 나중에는 여기서 DB를 조회해서 그날 쓴 메모를 보내주면 됩니다!
    return {
        "title": f"{date}의 공부 주제",
        "content": "이것은 서버에서 보낸 테스트 메모입니다."
    }