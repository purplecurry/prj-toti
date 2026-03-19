from sqlalchemy import Column, Integer, String, ForeignKey, select, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


# DB 관련된 정보를 사용해서 비동기 DB 엔진 생성.
DATABASE_URL = "sqlite+aiosqlite:///my_db.sqlite" 
engine = create_async_engine(DATABASE_URL, echo=True)

session_maker_function = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with session_maker_function() as db_session:
        yield db_session
        await db_session.commit()

class users(Base):
    __tablename__ = "users"
    id = Column(String(30), primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True)
    email = Column(String(100))
    hashed_password = Column(String(512))
    nickname = Column(String(50))
    goal_minutes = Column(Integer)
    focus_time = Column(Integer, default=25)
    break_time = Column(Integer, default=5)
    ai_mode = Column(String(20), default="cheer")
    created_at = Column(TIMESTAMP, server_default=func.now())

