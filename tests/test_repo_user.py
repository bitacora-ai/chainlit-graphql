import pytest
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.user import user_repo
from chainlit_graphql.model.user import User


@pytest.mark.asyncio
async def test_create_user(prepare_db):
    # Prepare user data
    user_data = User(
        email="user@example.com",
        password="hashed_password",  # Assume password is already hashed
        name="Test User",
        image=None,
        role="OWNER",
        # createdAt will be automatically set by the model
    )

    # Use the repository's create method to add the user
    created_user = await user_repo.create(user_data)

    assert created_user is not None
    assert created_user.email == "user@example.com"
    assert created_user.name == "Test User"


@pytest.mark.asyncio
async def test_get_by_email(prepare_db):
    async with db.SessionLocal() as session:
        email = "user2@example.com"
        user_data = User(
            email=email,
            password="hashed_password_here",  # Assuming password is already hashed
            name="Test User 2",
            role="OWNER",
            # createdAt is automatically set
        )
        session.add(user_data)
        await session.commit()

        result = await user_repo.get_by_email(email=email)
        assert result is not None
        assert result.email == email
        assert result.name == "Test User 2"
