from chainlit_graphql.model.feedback import Feedback
from chainlit_graphql.db.database import db
from sqlalchemy.sql import select
from typing import Optional


class FeedbackRepository:

    @staticmethod
    async def create(feedback_data: Feedback) -> Feedback:
        async with db as session:
            async with session.begin():
                session.add(feedback_data)
            await session.commit()

            result = await session.execute(
                select(Feedback).where(Feedback.id == feedback_data.id)
            )
            feedback = result.scalars().one()

            return feedback

    @staticmethod
    async def update(id: str, model: Feedback) -> Optional[Feedback]:
        async with db as session:
            stmt = select(Feedback).where(Feedback.id == id)
            result = await session.execute(stmt)
            existing_model = result.scalars().first()

            if existing_model:
                existing_model.comment = model.comment
                existing_model.value = model.value
                existing_model.strategy = model.strategy

                await session.commit()
                return existing_model
            else:
                return None


feedback_repo = FeedbackRepository()
