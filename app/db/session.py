from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import config

engine = create_async_engine(config.db_async_url)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
