from chainlit_graphql.model.apikey import ApiKey
from chainlit_graphql.db.database import db
from sqlalchemy.sql import select


class ApikeyRepository:

    @staticmethod
    async def create(apikey_data: ApiKey) -> ApiKey:
        async with db as session:
            async with session.begin():
                session.add(apikey_data)
            await session.commit()

            result = await session.execute(
                select(ApiKey).where(ApiKey.id == apikey_data.id)
            )
            apikey = result.scalars().one()

            return apikey

    @staticmethod
    async def get_by_key(key: str) -> ApiKey:
        async for session in db.get_db():
            stmt = select(ApiKey).where(ApiKey.key == key)
            result = await session.execute(stmt)
            key: ApiKey = result.scalars().first()
            if key:
                # Construct and return a ApiKey
                return key
            # Return None if no key is found
            return None


apikey_repo = ApikeyRepository()
