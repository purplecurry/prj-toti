from db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
# 민지님이 만든 설정 파일들을 불러옵니다
from db import get_db 
import models 

router = APIRouter(
    prefix="/calendar", # 모든 주소 앞에 /calendar가 붙습니다
    tags=["calendar"]
)

# 1. 특정 날짜의 투두 리스트(체크리스트) 가져오기
@router.get("/todos/{selected_date}")
def get_todos(selected_date: date, db: Session = Depends(get_db)):
    # DB에서 해당 날짜와 일치하는 투두들만 골라냅니다
    return db.query(models.Todo).filter(models.Todo.date == selected_date).all()

# 2. 새로운 투두(할 일) 추가하기
@router.post("/todos")
def create_todo(content: str, selected_date: date, db: Session = Depends(get_db)):
    new_todo = models.Todo(
        user_id=1, # 로그인 기능 합치기 전까지 임시로 1번 유저
        date=selected_date,
        content=content,
        is_completed=False
    )
    db.add(new_todo)
    db.commit()
    return {"message": "할 일이 저장되었습니다!"}

# 3. 메모(긴 글) 저장하기
@router.post("/memos")
def create_memo(title: str, content: str, db: Session = Depends(get_db)):
    new_memo = models.Memo(
        user_id=1,
        title=title,
        content=content
    )
    db.add(new_memo)
    db.commit()
    return {"message": "메모가 저장되었습니다!"}