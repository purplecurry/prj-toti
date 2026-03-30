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
    goal_achieved: bool,   # 프론트에서 보내는 값은 참고용
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 오늘 날짜 기록이 이미 있는지 확인
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == current_user.id,
            StudyRecord.date == target_date
        )
    )
    record = result.scalars().first()

    if record:
        # 누적 업데이트
        record.total_minutes += total_minutes
        record.completed_sessions += completed_sessions
    else:
        # 새로 생성
        record = StudyRecord(
            user_id=current_user.id,
            date=target_date,
            total_minutes=total_minutes,
            completed_sessions=completed_sessions,
            goal_achieved=False  # 일단 False로 생성
        )
        db.add(record)

    # 목표 달성 여부 자동 계산
    if record.total_minutes >= current_user.goal_minutes:
        record.goal_achieved = True
    else:
        record.goal_achieved = False

    await db.commit()
    return {"message": "저장 완료", "goal_achieved": record.goal_achieved}

# 일별 통계
@stats_router.get("/daily")
async def get_daily_stats(
    target_date: date,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == current_user.id,
            StudyRecord.date == target_date
        )
    )
    return result.scalars().first()

# 주간 통계
@stats_router.get("/weekly")
async def get_weekly_stats(
    year: int,
    week: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == current_user.id,
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
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == current_user.id,
            extract("year", StudyRecord.date) == year,
            extract("month", StudyRecord.date) == month
        )
    )
    return result.scalars().all()

# 년간 통계
@stats_router.get("/yearly")
async def get_yearly_stats(
    year: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudyRecord).where(
            StudyRecord.user_id == current_user.id,
            extract("year", StudyRecord.date) == year
        )
    )
    return result.scalars().all()
