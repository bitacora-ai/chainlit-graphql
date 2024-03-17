import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from chainlit_graphql.service.user import UserService
from chainlit_graphql.repository.user import UserRepository
from chainlit_graphql.model.user import User
from chainlit_graphql.api.v1.graphql.schema.user import UserType, RegisterInput


@pytest.fixture
def user_service():
    user_repo = (
        UserRepository()
    )  # Assuming the UserRepository does not require any arguments
    return UserService(user_repo)


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.user.get_password_hash", return_value="hashed_password"
)
@patch(
    "chainlit_graphql.repository.user.UserRepository.get_by_email",
    new_callable=AsyncMock,
)
@patch("chainlit_graphql.repository.user.UserRepository.create", new_callable=AsyncMock)
async def test_add_user(
    mock_create, mock_get_by_email, mock_get_password_hash, user_service
):
    email = "user@example.com"
    password = "securepassword"
    name = "Test User"
    image = "https://example.com/image.png"
    role = "OWNER"

    # Setup mock for get_by_email to return None, indicating no existing user
    mock_get_by_email.return_value = None

    # Setup the expected User model instance that create should return
    mock_user = User(
        id=1,
        email=email,
        password="hashed_password",
        name=name,
        image=image,
        role=role,
        createdAt=datetime.now(),
    )
    mock_create.return_value = mock_user

    # Prepare the RegisterInput data
    user_data = RegisterInput(email=email, password=password, name=name, image=image)

    # Call the add_user method
    result = await user_service.add_user(user_data)

    # Verify the results
    assert isinstance(result, UserType)
    assert result.email == email
    assert result.name == name
    assert result.image == image
    assert result.role == role

    # Ensure the get_by_email method was called with the correct email
    mock_get_by_email.assert_awaited_once_with(email)

    # Ensure the password hash function was called with the correct password
    mock_get_password_hash.assert_called_once_with(password)

    # Ensure the create method was called with a User instance containing the hashed password
    mock_create.assert_awaited_once()
    created_user_call_arg = mock_create.call_args.args[0]
    assert (
        created_user_call_arg.password == "hashed_password"
    ), "The password must be hashed before saving."
