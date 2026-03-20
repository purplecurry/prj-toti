from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base # 공통 DB 설정 (민지님과 공유)

# 동제님의 담당: 메모 모델
class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # 누가 썼는지
    date = Column(Date)                              # 어느 날짜인지
    content = Column(Text)                           # 메모 내용
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# 참고용: 민지님이 만들 공부 기록 모델
class StudyRecord(Base):
    __tablename__ = "study_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    total_minutes = Column(Integer, default=0)
    goal_achieved = Column(Boolean, default=False)