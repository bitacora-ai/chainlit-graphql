from chainlit_graphql.service.user import UserService
from chainlit_graphql.service.apikey import ApikeyService
from chainlit_graphql.repository.user import user_repo
from chainlit_graphql.repository.apikey import apikey_repo
from chainlit_graphql.api.v1.graphql.schema.user import RegisterInput
from chainlit_graphql.core.config import settings


async def create_initial_data():
    user_service = UserService(user_repo)
    apikey_service = ApikeyService(apikey_repo)

    # Define your initial user data
    initial_user_data = RegisterInput(
        email=settings.USER_EMAIL,
        password=settings.USER_PASSWORD,
        name=settings.USER_NAME,
        image=settings.USER_IMAGE_PATH,
    )

    # Create the initial user
    created_user = await user_service.add_user(initial_user_data)

    # Create an API key for the initial user
    if created_user:
        await apikey_service.create_apikey(
            name="Initial API Key",
            user_id=created_user.id,
            key=settings.LITERAL_API_KEY,
            project_id=settings.USER_PROJECT_ID,
        )
