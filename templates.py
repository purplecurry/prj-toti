from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/templates")

@router.get("/timer")
async def timer_page():
    file_path = os.path.join("templates","timer.html")
    return FileResponse(file_path)

@router.get("/login")
async def login():
    file_path = os.path.join("templates","login.html")
    return FileResponse(file_path)

@router.get("/mypage")
async def mypage():
    file_path = os.path.join("templates","mypage.html")
    return FileResponse(file_path)

@router.get("/settings")
async def settings():
    file_path = os.path.join("templates","settings.html")
    return FileResponse(file_path)

@router.get("/signup")
async def signup():
    file_path = os.path.join("templates","signup.html")
    return FileResponse(file_path)