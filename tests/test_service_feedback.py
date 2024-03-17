import pytest
from unittest.mock import patch, AsyncMock
from chainlit_graphql.service.feedback import FeedbackService
from chainlit_graphql.model.feedback import Feedback
from chainlit_graphql.repository.feedback import feedback_repo
from chainlit_graphql.api.v1.graphql.schema.feedback import (
    FeedbackType,
    FeedbackStrategy,
)


@pytest.fixture
def feedback_service():
    return FeedbackService(feedback_repo)


# Test for add_feedback
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.feedback.FeedbackRepository.create",
    new_callable=AsyncMock,
)
async def test_add_feedback(mock_create, feedback_service):
    comment = "Great job"
    stepId = "step-123"
    strategy = FeedbackStrategy.STARS
    value = 5
    mock_feedback = Feedback(
        id="feedback-123",
        comment=comment,
        step_id=stepId,
        strategy=strategy.value,
        value=value,
    )
    mock_create.return_value = mock_feedback

    result = await feedback_service.add_feedback(comment, stepId, strategy, value)

    assert isinstance(result, FeedbackType)
    assert result.id == mock_feedback.id
    assert result.comment == mock_feedback.comment
    assert result.stepId == mock_feedback.step_id
    assert result.strategy == mock_feedback.strategy
    assert result.value == mock_feedback.value
    mock_create.assert_awaited_once()


# Test for update
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.feedback.FeedbackRepository.update",
    new_callable=AsyncMock,
)
async def test_update_feedback(mock_update, feedback_service):
    feedback_id = "feedback-123"
    comment = "Updated comment"
    value = 4
    strategy = FeedbackStrategy.LIKERT
    mock_feedback = Feedback(
        id=feedback_id, comment=comment, value=value, strategy=strategy.value
    )
    mock_update.return_value = mock_feedback

    result = await feedback_service.update(feedback_id, comment, value, strategy)

    assert isinstance(result, FeedbackType)
    assert result.id == feedback_id
    assert result.comment == comment
    assert result.strategy == strategy.value
    assert result.value == value
    mock_update.assert_awaited_once_with(feedback_id, mock_feedback)
