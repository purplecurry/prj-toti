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
from db import get_db, User, Memo, PomodoroSession, SessionDetail
from user import SECRET_KEY, ALGORITHM, oauth2_scheme

router = APIRouter(prefix="/timer")

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


async def get_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not token:
        # 토큰이 없으면 바로 401
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

# # 임시 테스트용
# async def get_user_from_token(
#     token: str | None = None,   # 토큰 무시
#     db: AsyncSession = Depends(get_db)
# ) -> User:
#     # 임시로 항상 첫 번째 유저 반환
#     result = await db.execute(select(User).limit(1))
#     user = result.scalar_one_or_none()
#     if user:
#         await db.refresh(user)
#     if not user:
#         # 유저가 없으면 테스트용 더미 유저 생성
#         user = User(
#             email="test@example.com",
#             password="1234",
#             nickname="tester"
#         )
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)

#     return user



# ====엔드포인트====

# 타이틀 페이지(타이머)
@router.get("/")
async def timer_page():
    file_path = os.path.join("templates","timer.html")
    return FileResponse(file_path)

# 모바일 페이지 욕심을 위한 api 분리
@router.get("/api/timer-data")
async def timer_data(current_user:User=Depends(get_user_from_token), db: AsyncSession=Depends(get_db)):
    # 여기서는 로그인 필수 → 로그인 안 된 경우 이미 401 반환됨
    return {
        "logged_in": True,
        "focus_time": current_user.default_focus_time,
        "break_time": current_user.default_break_time,
    }

@router.get("/api/memos")
async def memos_data(current_user: User = Depends(get_user_from_token), db: AsyncSession=Depends(get_db)):
    result = await db.execute(
        select(Memo.id, Memo.title).filter(Memo.user_id == current_user.id)
    )
    rows = result.mappings().all()
    memos = [{"id": row["id"], "title": row["title"]} for row in rows]
    return {"memos": memos}


#메모 저장시 신규 작성 혹은 수정
@router.put("/memo/write")
async def memo_write(body:MemoWrite, current_user=Depends(get_user_from_token), db: AsyncSession=Depends(get_db)):

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

#메모 삭제
@router.delete("/memo/{memo_id}")
async def memo_delete(memo_id: int, current_user=Depends(get_user_from_token), db: AsyncSession=Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    result = await db.execute(
        select(Memo).filter(Memo.id == memo_id, Memo.user_id == current_user.id)
    )
    memo = result.scalar_one_or_none()

    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")

    await db.delete(memo)
    await db.commit()

    return {"message": "메모 삭제 완료!", "id": memo_id}

#프론트에서 메모 타이틀 클릭시 해당 메모 content 호출
@router.get("/memo/{memo_id}")
async def memo_content(memo_id: int, current_user=Depends(get_user_from_token), db: AsyncSession=Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    result = await db.execute(select(Memo).filter(Memo.id == memo_id, Memo.user_id == current_user.id))
    memo = result.scalar_one_or_none()

    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    
    return {"id": memo.id, "title": memo.title, "content": memo.content}

#프론트에서 타이머 종료시 해당 세션 저장
@router.post("/session-end")
async def session_end(body:SessionResult, current_user=Depends(get_user_from_token), db: AsyncSession=Depends(get_db)):

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

