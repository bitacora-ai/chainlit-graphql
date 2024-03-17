from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from chainlit_graphql.core.config import settings


class DatabaseSession:
    def __init__(self, url: str = settings.DATABASE_URI.unicode_string()):
        self.engine = create_async_engine(url, echo=False)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self):
        await self.engine.dispose()

    async def __aenter__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


db = DatabaseSession()
