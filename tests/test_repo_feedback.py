import pytest
from chainlit_graphql.api.v1.graphql.schema.feedback import FeedbackStrategy
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.feedback import feedback_repo
from chainlit_graphql.model import Feedback


@pytest.mark.asyncio
async def test_create_feedback(prepare_db):
    async with db.SessionLocal():
        # Adjust attribute to thread_id
        feedback_data = Feedback(
            id="feedback-1",
            thread_id="thread-1",
            value=5.0,
            strategy=FeedbackStrategy.STARS.value,
            comment="Great!",
        )
        created_feedback = await feedback_repo.create(feedback_data)
        assert created_feedback.id == feedback_data.id
        assert created_feedback.thread_id == feedback_data.thread_id  # Use thread_id
        assert created_feedback.value == feedback_data.value
        # Compare with the enum's value
        assert created_feedback.strategy == FeedbackStrategy.STARS.value
        assert created_feedback.comment == feedback_data.comment


@pytest.mark.asyncio
async def test_update_feedback(prepare_db):
    async with db.SessionLocal() as session:
        feedback_data = Feedback(
            id="feedback-2",
            thread_id="thread-2",
            value=3.0,
            strategy=FeedbackStrategy.LIKERT.value,
            comment="Good",
        )
        session.add(feedback_data)
        await session.commit()

        updated_model = Feedback(
            id="feedback-2",
            comment="Updated comment",
            value=4.5,
            strategy=FeedbackStrategy.BIG_STARS.value,
        )
        updated_feedback = await feedback_repo.update("feedback-2", updated_model)
        assert updated_feedback.comment == "Updated comment"
        assert updated_feedback.value == 4.5
        assert updated_feedback.strategy == FeedbackStrategy.BIG_STARS.value
