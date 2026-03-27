from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    is_completed = Column(Boolean, default=False)
    date = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

# StudyRecord (또는 DailyMemo) 클래스
class StudyRecord(Base):  # 이름을 StudyRecord로 통일합니다.
    __tablename__ = "study_records"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

# 혹시 다른 파일에서 DailyMemo라는 이름을 쓸 수도 있으니 별칭을 만들어둡니다.
DailyMemo = StudyRecord