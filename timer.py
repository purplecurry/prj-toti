from fastapi import APIRouter, Request, Depends
from fastapi import Form, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/timer", response_class=HTMLResponse)
async def timer(request: Request, signin_data: user.UserLogin, db_session: AsyncSession = Depends(get_db_session))
    pass