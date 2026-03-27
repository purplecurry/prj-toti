# my_calendar.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from models import Todo, StudyRecord  # 1단계에서 만든 모델 가져오기

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get("/calendar")
async def get_calendar():
    return {"message": "calendar view"}

# 1. 월간 요약 (나중에 DB 연동 가능)
@router.get("/summary/{year}/{month}")
async def get_month_summary(year: int, month: int, db: AsyncSession = Depends(get_db)):
    return {
        "year": year, 
        "month": month, 
        "results": [{"day": 1, "status": 1}]
    }

# 2. 특정 날짜 정보 조회 (DB에서 진짜 가져오기)
@router.get("/daily/{date}")
async def get_daily_info(date: str, db: AsyncSession = Depends(get_db)):
    # DB에서 해당 날짜의 Todo들 찾기
    result = await db.execute(select(Todo).where(Todo.date == date))
    todos = result.scalars().all()
    
    return {
        "date": date,
        "todos": todos,
        "memo": "열심히 하자!" # 메모 테이블도 만들면 나중에 연동!
    }

# 3. 진짜 Todo 추가 (DB 저장 적용)
@router.post("/todo")
async def add_todo(content: str, date: str, db: AsyncSession = Depends(get_db)):
    # 2단계: 진짜 DB 객체 생성
    new_todo = Todo(content=content, date=date, user_id=1) 
    db.add(new_todo)
    await db.commit() # 반드시 await가 있어야 진짜 저장이 됩니다!
    return {"message": "저장 성공"}

# 4. 진짜 학습 시간 기록 (DB 저장 적용)
@router.post("/study-record")
async def record_study(minutes: int, date: str, db: AsyncSession = Depends(get_db)):
    new_record = StudyRecord(minutes=minutes, date=date, user_id=1)
    
    db.add(new_record)
    await db.commit()
    
    return {
        "status": "success",
        "study_time": f"{minutes} minutes",
        "timestamp": datetime.now().isoformat() # ISO 8601 형식
    }