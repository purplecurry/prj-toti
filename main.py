from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
import ai_service, calendar, db, timer, user


@asynccontextmanager
async def app_life_span(app: FastAPI):
    # 비동기 엔진으로 테이블을 생성하는 올바른 방법입니다
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=app_life_span)

app.include_router(timer.router)