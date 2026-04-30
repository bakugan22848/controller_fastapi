from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from app.core.config import settings as stt

DB_URL = f"postgresql+asyncpg://{stt.DB_USER}:{stt.DB_PASSWORD}@{stt.DB_HOST}:{stt.DB_PORT}/{stt.DB_NAME}"

engine: create_async_engine = create_async_engine(
    DB_URL,
    pool_size=40,
    max_overflow=10,
    echo=True,
)

AsyncSessionLocal: async_sessionmaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit = False,
    autoflush = False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

metadata_obj = MetaData()
Base = declarative_base(metadata=metadata_obj)