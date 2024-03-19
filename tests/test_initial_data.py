import pytest
from sqlalchemy import select
from chainlit_graphql.db.initial_data import create_initial_data
from chainlit_graphql.model.user import User
from chainlit_graphql.model.apikey import ApiKey
from chainlit_graphql.db.database import db


@pytest.mark.asyncio
async def test_create_initial_data(prepare_db):
    # Assuming prepare_db properly prepares your test database
    await create_initial_data()

    # Verify the created user in the database
    async with db.SessionLocal() as session:
        async with session.begin():
            # Query for the created user by email
            user = await session.execute(
                select(User).where(User.email == "initial@example.com")
            )
            user = user.scalars().first()

            # Ensure the user was created
            assert user is not None
            assert user.email == "initial@example.com"
            assert user.password != "initialPassword"  # Assuming the password is hashed
            assert user.name == "Initial User"
            assert user.image == "/path/to/image.jpg"

            # Query for the created API key using the user's ID
            apikey = await session.execute(
                select(ApiKey).where(ApiKey.user_id == user.id)
            )
            apikey = apikey.scalars().first()

            # Ensure the API key was created for the user
            assert apikey is not None
            assert apikey.key, "apikey.key is None or empty"
            assert apikey.name == "Initial API Key"
            assert apikey.project_id == "PROJECT_ID_HERE"
