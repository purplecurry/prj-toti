from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract
from db import get_db, StudyRecord
from user import get_current_user
from datetime import date

router = APIRouter()
stats_router = APIRouter(prefix="/stats")

# 세션 저장
@router.post("/sessions")
async def create_session(
    target_date: date,
    total_minutes: int,
    completed_sessions: int,
    goal_achieved: bool,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    record = StudyRecord(
        user_id=user_id,
        date=target_date,
        total_minutes=total_minutes,
        completed_sessions=completed_sessions,
        goal_achieved=goal_achieved
    )
    db.add(record)
    await db.commit()
    return {"message": "저장 완료"}

# 일별 통계
@stats_router.get("/daily")
async def get_daily_stats(
    target_date: date,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == user_id,
            StudyRecord.date == target_date
        )
    )
    return result.scalars().first()

# 주간 통계
@stats_router.get("/weekly")
async def get_weekly_stats(
    year: int,
    week: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == user_id,
            extract("year", StudyRecord.date) == year,
            extract("week", StudyRecord.date) == week
        )
    )
    return result.scalars().all()

# 월간 통계
@stats_router.get("/monthly")
async def get_monthly_stats(
    year: int,
    month: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == user_id,
            extract("year", StudyRecord.date) == year,
            extract("month", StudyRecord.date) == month
        )
    )
    return result.scalars().all()

# 년간 통계
@stats_router.get("/yearly")
async def get_yearly_stats(
    year: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == user_id,
            extract("year", StudyRecord.date) == year
        )
    )
    return result.scalars().all()