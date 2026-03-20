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


@router.get("/timer")
async def read_root(request:Request, db: AsyncSession=Depends(get_db_session)):
    result = await db.execute(select(users).where(users.id == request.session.get("id")))
    user = result.scalars().first()

    focust_time = user.default_focus_time if user else 25
    break_time = user.default_break_time if user else 5

    return templates.TemplateResponse("timer.html", {"request":request, "focus_time":focust_time, "break_time":break_time,})

