from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import ai_service, my_calendar, db, timer, user, stats
import os
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db, Todo  # Todo 모델이 db.py에 있다고 가정할게요!
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 접속 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 절대 경로 구하기
base_path = os.path.dirname(os.path.abspath(__file__))

# 2. 다른 모든 경로(@app.get 등)보다 먼저 마운트하기! (중요)
app.mount("/static", StaticFiles(directory=base_path), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 1. 데이터 형식 정의 (이게 있어야 422 에러가 안 나요!)
class MemoCreate(BaseModel):
    title: str
    content: str
    user_id: int

from fastapi import Request # 상단에 있는지 확인

@app.post("/memo")
async def create_memo(title: str, content: str, date: str, user_id: int):
    # [기상님 미션: 실제 AI 연동]
    # 실제로는 아래와 유사한 코드가 들어가야 합니다.
    # advice = await ai_service.generate_feedback(content) 
    
    # 임시로 AI 기분을 내려면 이렇게 바꿔보세요:
    advice = f"와! '{title}' 공부를 하셨군요! {content} 내용을 보니 오늘 정말 알차게 보내신 것 같아요. 토마토 하나 더 드릴게요! 🍅"

    return {
        "status": "success", 
        "ai_advice": advice  # 👈 이제 "저장 성공" 대신 진짜 조언이 나갑니다!
    }

# 1. 템플릿(HTML) 폴더 설정 (에러 해결!)
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def app_life_span(app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=app_life_span)

# 라우터 연결
app.include_router(timer.router)
app.include_router(my_calendar.router)
app.include_router(user.router)
app.include_router(stats.router)

# 2. 첫 화면 설정 (calendar.html 띄우기)
@app.get("/timer")  # 혹은 @app.get("/mycalendar")
async def get_timer(request: Request):
    return templates.TemplateResponse("timer.html", {"request": request})

@app.post("/todo")
async def create_todo(content: str, user_id: int, date: str, db: AsyncSession = Depends(get_db)):
    new_todo = Todo(content=content, user_id=user_id, date=date) # 1. 새로운 할 일 객체 만들기
    db.add(new_todo)        # 2. 장부에 적기
    await db.commit()      # 3. 도장 쾅! (실제 저장)
    await db.refresh(new_todo) # 4. 저장된 데이터 확인
    return {"status": "success", "todo": new_todo.content}

from fastapi import Body # 파일 상단에 Body가 있는지 확인!

@app.post("/memo")
async def create_memo(title: str, content: str, date: str, user_id: int):
    # ✅ 1. 이 줄부터는 무조건 '들여쓰기(Tab 또는 스페이스 4칸)'가 되어야 합니다!
    print(f"🚀 데이터 수신 성공: {title}, {content}")

    # ✅ 2. 기상님 미션: 동제님이 쓴 제목과 내용을 읽어서 응답하기
    return {
        "status": "success", 
        "ai_advice": f"동제님, '{title}' 주제 공부를 시작하셨군요! '{content}' 내용을 보니 정말 멋져요! 🍅"
    }