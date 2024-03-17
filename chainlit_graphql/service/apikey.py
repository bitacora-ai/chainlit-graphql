import secrets
from chainlit_graphql.repository.apikey import ApikeyRepository
from chainlit_graphql.model.apikey import ApiKey


class ApikeyService:
    def __init__(self, apikey_repository: ApikeyRepository):
        self.apikey_repository = apikey_repository

    async def create_apikey(
        self, name: str, user_id: int, project_id: str, key: str = None
    ) -> ApiKey:
        # If no key is provided, generate a secure, random API key
        if key is None:
            key = secrets.token_urlsafe(32)

        # Check if the API key already exists
        apikey_instance = await self.apikey_repository.get_by_key(key)
        if apikey_instance:
            # Return the existing API key if found
            return apikey_instance

        # Proceed with creating a new API key if it doesn't exist
        apikey_instance = ApiKey(
            key=key, name=name, user_id=user_id, project_id=project_id
        )
        created_apikey = await self.apikey_repository.create(apikey_instance)

        return created_apikey

    async def validate_apikey(self, key: str) -> ApiKey:
        """
        Validates an API key by checking if it exists in the database.

        :param key: The API key to validate.
        :return: The ApiKey model instance if the key is valid, None otherwise.
        """
        # Use the repository to get the ApiKey instance by its key
        apikey_instance = await self.apikey_repository.get_by_key(key)

        return apikey_instance
