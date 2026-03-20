from fastapi import APIRouter, Request, Depends
from fastapi import Form, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
import user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db_session, users

router = APIRouter()
templates = Jinja2Templates(directory="templates")

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db_session)):
    user_id = request.session.get("id")
    if not user_id:
        return None
    result = await db.execute(select(users).where(users.id == user_id))
    user = result.scalars().first()
    return user

@router.get("/timer")
async def timer(request:Request, current_user=Depends(get_current_user),db: AsyncSession=Depends(get_db_session)):
    
    focust_time = await current_user.default_focus_time if current_user else 25
    break_time = await current_user.default_break_time if current_user else 5

    return templates.TemplateResponse("timer.html", {"request":request, "focus_time":focust_time, "break_time":break_time,})

@router.get("/timer/memo")
async def read_memo(request:Request, db: AsyncSession=Depends(get_db_session)):
    
