from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from db import Base
from datetime import datetime

# 1. 메모 모델 (동제님 담당)
class Memo(Base):
    __tablename__ = "memos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # 누가 썼는지
    date = Column(String)                 # 날짜: YYYY-MM-DD
    content = Column(Text)                # 메모 내용
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# 2. 할 일 모델 (동제님 담당)
class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) 
    content = Column(String)              # 할 일 내용
    date = Column(String)                 # 날짜: YYYY-MM-DD
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

# 3. 학습 기록 모델 (민지님 규칙 반영: 분 단위)
class StudyRecord(Base):
    __tablename__ = "study_records"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    minutes = Column(Integer, default=0)  # 시간: 분 단위 (민지님 규칙!)
    date = Column(String)                 # 날짜: YYYY-MM-DD
    goal_achieved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())