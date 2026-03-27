from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import ai_service, my_calendar, db, timer, user, stats

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

# 2. 첫 화면 설정 (index.html 띄우기)
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})