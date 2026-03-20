from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 비동기용 SQLite 주소 (앞에 +aiosqlite가 붙어야 합니다)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# 1. 비동기 엔진 생성
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 2. 비동기 세션 메이커
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# 3. 비동기용 get_db 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session