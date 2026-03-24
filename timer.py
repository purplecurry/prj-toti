from fastapi import APIRouter, Depends, Response
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional
import os
from .db import get_db, User, Memo, PomodoroSession, SessionDetail
from .user import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/timer")

# 로그인 확인 분기용 스키마. user와 달리 로그인이 필수가 아닌 영역들이 있음
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)

# =====pydantic=====
class SessionResult(BaseModel):
    started_at : datetime
    ended_at : datetime
    duration : int

class MemoWrite(BaseModel):
    id: Optional[int] = None
    title: str
    content: str

# =======유틸========

async def get_user_from_uid(
    token: str | None = Depends(optional_oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    
    # 토큰이 아예 없으면 (비로그인) 즉시 None 반환
    if not token:
        return None
        
    try:
        # 2. 직접 토큰 복호화 (다른 사람 코드 의존성 제거)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if user_id is None:
            return None
            
        # 3. DB에서 유저 조회
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        return user
        
    except (JWTError, HTTPException):
        # 토큰 변조, 만료 등 어떤 에러가 나도 비로그인 취급(None)
        return None

# ====엔드포인트====

# 이틀 페이지(타이머)
@router.get("/")
async def timer_page():
    file_path = os.path.join("templates","timer.html")
    return FileResponse(file_path)

# 모바일 페이지 욕심을 위한 api 분리
@router.get("/api/timer-data")
async def timer_data(current_user = Depends(get_user_from_uid), db:AsyncSession = Depends(get_db)):
    focus_time = current_user.default_focus_time if current_user else 25
    break_time = current_user.default_break_time if current_user else 5
    memos = []
    if current_user:
        result = await db.execute(
            select(Memo.id, Memo.title).filter(Memo.user_id == current_user.id)
        )
        memos = [{"id": m.id, "title": m.title} for m in result.all()]
    # TODO: (가능하면) bgm 기능 추가시 가져오기
    return {
        "focus_time": focus_time,
        "break_time": break_time,
        "memos": memos
    }

#메모 저장시 신규 작성 혹은 수정
@router.put("/memo/write")
async def memo_write(body=MemoWrite, current_user=Depends(get_user_from_uid), db: AsyncSession=Depends(get_db)):

    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    if body.id:
        memo_id = body.id

        result = await db.execute(
            select(Memo).filter(Memo.id  == memo_id, Memo.user_id == current_user.id)
        )    
        memo = result.scalar_one_or_none()
        if memo:
            memo.title = body.title
            memo.content = body.content
            memo.updated_at = func.now()
        else:
            raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    else:
        memo = Memo(
            user_id = current_user.id,
            title=body.title,
            content=body.content,
        )
        db.add(memo)
    
    await db.commit()
    await db.refresh(memo)
    return {"message":"메모 저장 완료!", "memo": {"id": memo.id, "title": memo.title, "content": memo.content}}


#프론트에서 메모 타이틀 클릭시 해당 메모 content 호출
@router.get("/memo/{memo_id}")
async def memo_content(memo_id: int, current_user=Depends(get_user_from_uid), db: AsyncSession=Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    result = await db.execute(select(Memo).filter(Memo.id == memo_id, Memo.user_id == current_user.id))
    memo = result.scalar_one_or_none()

    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    
    return {"id": memo.id, "title": memo.title, "content": memo.content}

#프론트에서 타이머 종료시 해당 세션 저장
@router.post("/session-end")
async def session_end(body=SessionResult, current_user=Depends(get_user_from_uid), db: AsyncSession=Depends(get_db)):

    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    result = await db.execute(select(PomodoroSession).filter(PomodoroSession.user_id == current_user.id, PomodoroSession.date == date.today()))
    pomodoro_session = result.scalar_one_or_none()

    if not pomodoro_session:
        pomodoro_session = PomodoroSession(
            user_id = current_user.id,
            date=date.today()
        )
        db.add(pomodoro_session)
        await db.commit()
        await db.refresh(pomodoro_session)

    session_detail = SessionDetail(
        session_id = pomodoro_session.id,
        started_at = body.started_at,
        ended_at = body.ended_at,
        duration = body.duration,
        is_completed = True,
    )
    db.add(session_detail)
    
    pomodoro_session.total_duration += body.duration

    await db.commit()
    await db.refresh(session_detail)
    await db.refresh(pomodoro_session)
    
    return Response(status_code=204)

