from chainlit_graphql.model.feedback import Feedback
from chainlit_graphql.repository.feedback import FeedbackRepository
from chainlit_graphql.api.v1.graphql.schema.feedback import (
    FeedbackType,
    FeedbackStrategy,
)
from typing import Optional


class FeedbackService:
    def __init__(self, feedback_repository: FeedbackRepository):
        self.feedback_repository = feedback_repository

    async def add_feedback(
        self,
        comment: Optional[str],
        stepId: str,
        strategy: Optional[FeedbackStrategy],
        value: int,
    ) -> FeedbackType:

        # Create and save the new Feedback
        feedback = await self.feedback_repository.create(
            Feedback(
                comment=comment,
                step_id=stepId,
                strategy=strategy if strategy.value else None,
                value=value,
            )
        )

        return FeedbackType(
            id=feedback.id,
            comment=feedback.comment,
            stepId=feedback.step_id,
            strategy=feedback.strategy,
            value=feedback.value,
            threadId=feedback.thread_id,
        )

    async def update(
        self,
        id: str,
        comment: Optional[str],
        value: Optional[int],
        strategy: Optional[FeedbackStrategy],
    ) -> FeedbackType:
        # Convert the strategy enum to its string value if it's not None; otherwise, pass None
        strategy_str = strategy.value if strategy else None

        # Create the feedback object with the strategy as a string
        feedback_to_update = Feedback(
            id=id, comment=comment, value=value, strategy=strategy_str
        )

        updated_feedback = await self.feedback_repository.update(id, feedback_to_update)

        if updated_feedback:
            # Return a FeedbackType object, assuming FeedbackType is properly defined to handle the attributes
            return FeedbackType(
                id=updated_feedback.id,
                comment=updated_feedback.comment,
                stepId=updated_feedback.step_id,
                strategy=updated_feedback.strategy,
                value=updated_feedback.value,
                threadId=updated_feedback.thread_id,
            )
        else:
            raise ValueError(f"Feedback with id {id} not found")
