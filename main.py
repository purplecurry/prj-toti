from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
import ai_service, my_calendar, db, timer, user, stats


@asynccontextmanager
async def app_life_span(app: FastAPI):
    # 비동기 엔진으로 테이블을 생성하는 올바른 방법입니다
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=app_life_span)

app.include_router(timer.router)
app.include_router(my_calendar.router)
app.include_router(ai_service.router)
app.include_router(user.router)
app.include_router(stats.router)
app.include_router(stats.stats_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/timer")