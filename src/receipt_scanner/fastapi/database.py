from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import sessionmaker

SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./note.db"

async_engine = create_async_engine(SQLITE_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


def get_async_session() -> AsyncSession:
    return AsyncSessionLocal()
