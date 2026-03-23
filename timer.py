# timer.py 파일의 맨 위에 추가
# timer.py 맨 윗부분
from sqlalchemy.ext.asyncio import AsyncSession  # <-- 이 줄이 빠져서 에러가 난 거예요!
from db import get_db
import user
from db import get_db
from fastapi import Depends, Request  # Request나 Depends가 없다고 뜰 수도 있으니 같이 확인!
from fastapi import APIRouter, Request, Depends
from fastapi import Form, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from user import get_current_user, oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/timer", response_class=HTMLResponse)
async def timer(request: Request, signin_data: dict, db_session: AsyncSession = Depends(get_db)):
    pass