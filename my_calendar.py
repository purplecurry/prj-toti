# my_calendar.py
from fastapi import APIRouter

# 이 줄이 반드시 있어야 main.py에서 가져다 쓸 수 있습니다!
router = APIRouter()

@router.get("/calendar")
async def get_calendar():
    return {"message": "calendar view"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
# models.py에 Todo와 Memo 클래스가 있다고 가정할 때의 예시입니다.
# from models import Todo, Memo 

# 1. 월간 토마토 상태 조회 (0: 없음, 1: 일반, 2: 골든)
@router.get("/summary/{year}/{month}")
async def get_month_summary(year: int, month: int, db: AsyncSession = Depends(get_db)):
    # 지금은 테스트용 가짜 데이터를 보내줄게요. 나중에 DB 로직을 채우면 됩니다!
    return {
        "year": year, 
        "month": month, 
        "results": [
            {"day": 1, "status": 1}, 
            {"day": 2, "status": 2}
        ]
    }

# 2. 특정 날짜의 할 일(Todo) 및 메모 조회
@router.get("/daily/{date}")
async def get_daily_info(date: str, db: AsyncSession = Depends(get_db)):
    # date 형식: "2026-03-23"
    return {
        "date": date,
        "todos": [{"id": 1, "task": "코딩하기", "done": True}],
        "memo": {"title": "주간 목표", "content": "열심히 하자!"}
    }

# 3. 새로운 Todo 추가
@router.post("/todo")
async def add_todo(content: str, date: str, db: AsyncSession = Depends(get_db)):
    return {"message": "Todo가 추가되었습니다.", "content": content}