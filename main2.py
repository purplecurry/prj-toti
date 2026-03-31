from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 기존 모듈들 연결
import db, timer, my_calendar, ai_service, user, stats

# 1. 앱 수명 주기 관리 (기상님 스타일 그대로 유지)
@asynccontextmanager
async def app_life_span(app: FastAPI):
    async with db.engine.begin() as conn:
        # DB 테이블 자동 생성 (db.py의 설정을 따름)
        await conn.run_sync(db.Base.metadata.create_all)
    yield    

# 2. FastAPI 앱 초기화
app = FastAPI(lifespan=app_life_span)

# 3. 정적 파일 설정
app.mount("/bgms", StaticFiles(directory="bgms"), name="bgms")
# templates 폴더 연결 (my_calendar 등에서 사용)
templates = Jinja2Templates(directory="templates")

# 4. 모든 라우터 연결 (기상님 main.py와 동일하게 유지)
app.include_router(timer.router)
app.include_router(my_calendar.router)  # 동제님이 고친 calendar 기능 연결!
app.include_router(ai_service.router)
app.include_router(user.router)
app.include_router(stats.router)
app.include_router(stats.stats_router)

# 5. 기본 접속 시 타이머로 리다이렉트
@app.get("/")
async def root():
    return RedirectResponse(url="/timer")

# 6. (선택사항) .env 환경 변수 로드가 필요한 경우 여기에 추가 가능
# 예: print("시스템 준비 완료!")