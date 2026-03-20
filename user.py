from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

# 1. 기상님이 timer.py에서 찾던 바로 그 클래스!
class UserLogin(BaseModel):
    email: str
    password: str

# 2. 나중에 연주님이 구현할 기본 회원가입 구조
class UserCreate(BaseModel):
    email: str
    password: str
    nickname: str

@router.post("/login")
def login(data: UserLogin):
    return {"message": "임시 로그인 성공", "email": data.email}