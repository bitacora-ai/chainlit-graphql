from chainlit_graphql.model.user import User
from chainlit_graphql.api.v1.graphql.schema.user import UserType, RegisterInput
from chainlit_graphql.repository.user import UserRepository
from chainlit_graphql.core.security import get_password_hash


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def add_user(self, user_data: RegisterInput) -> UserType:
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            # Instead of raising an error, return the existing user
            return UserType(
                id=existing_user.id,
                email=existing_user.email,
                image=existing_user.image,
                name=existing_user.name,
                role=existing_user.role,
            )

        # Hash the password before saving
        hashed_password = get_password_hash(user_data.password)

        created_user = await self.user_repository.create(
            User(
                email=user_data.email,
                password=hashed_password,
                name=user_data.name if hasattr(user_data, "name") else None,
                image=user_data.image if hasattr(user_data, "image") else None,
            )
        )

        return UserType(
            id=created_user.id,
            email=created_user.email,
            image=created_user.image,
            name=created_user.name,
            role=created_user.role,
        )
