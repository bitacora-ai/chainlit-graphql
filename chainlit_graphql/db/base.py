from .database import db
from sqlmodel import SQLModel


async def create_all():
    async with db.engine.begin() as conn:
        # Use SQLModel's meta_data to create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_all():
    async with db.engine.begin() as conn:
        # Use SQLModel's metadata to drop all tables
        await conn.run_sync(SQLModel.metadata.drop_all)
