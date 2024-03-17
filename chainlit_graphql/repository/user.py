from chainlit_graphql.api.v1.graphql.schema.user import UserType
from chainlit_graphql.model.user import User
from chainlit_graphql.db.database import db
from sqlalchemy.sql import select
from typing import Optional


class UserRepository:

    @staticmethod
    async def create(user_data: User) -> User:
        async for session in db.get_db():
            async with session.begin():
                # Add the new user to the session
                session.add(user_data)

                # Flush the session to ensure the user is persisted
                await session.flush()

                # Refresh the instance to get any updated attributes from the database
                await session.refresh(user_data)

                # Commit the transaction
                await session.commit()

        # Return the newly created user
        return user_data

    @staticmethod
    async def get_by_email(email: str) -> Optional[UserType]:
        async for session in db.get_db():
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user: User = result.scalars().first()
            if user:
                # Construct and return a UserType
                return UserType(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    image=user.image,
                    role=user.role,
                )
            # Return None if no user is found
            return None


user_repo = UserRepository()
