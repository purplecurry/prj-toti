from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
import ai_service, calendar, db, timer, user

from stats import router, stats_router
app.include_router(router)
app.include_router(stats_router)


@asynccontextmanager
async def app_life_span(app: FastAPI):
    async with db.engine.begin() as conn:                  # 종료하면 자동으로 닫힌다.
        await conn.run_sync(db.Base.metadata.create_all)   # 동기 실행 ==> 비동기 실행.
    yield    

app = FastAPI(lifespan=app_life_span)

app.include_router(timer.router)