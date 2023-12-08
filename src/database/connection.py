from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import (
    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
    POSTGRES_HOST, POSTGRES_PORT
)


DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa

engine = create_async_engine(DATABASE_URL)

Session = sessionmaker(
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)

Base = declarative_base()
