from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.env import EnvConfig
from typing import AsyncGenerator

env_config = EnvConfig() # type: ignore

engine = create_async_engine(env_config.DATABASE_URI)

async_session_factory = sessionmaker(
    bind=engine, # type: ignore
    class_=AsyncSession,
    expire_on_commit=False
) # type: ignore

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session: # type: ignore
            yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db():
    async with engine.connect() as conn:
        try:
            yield conn
        finally:
            await conn.close()
