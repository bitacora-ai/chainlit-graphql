import pytest
from unittest.mock import patch, AsyncMock
from chainlit_graphql.service.score import ScoreService
from chainlit_graphql.model.score import Score as ModelScore
from chainlit_graphql.repository.score import score_repo
from chainlit_graphql.api.v1.graphql.schema.score import ScoreType, Score as SchemaScore


@pytest.fixture
def score_service():
    return ScoreService(score_repo)


# Test for add_score
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.score.ScoreRepository.create",
    new_callable=AsyncMock,
)
async def test_add_score(mock_create, score_service):
    id = "score-123"
    name = "Test Score"
    type = ScoreType.AI  # Assuming ScoreType.AI is the correct enum value
    value = 95.5
    stepId = "step-123"
    generationId = "gen-123"
    datasetExperimentItemId = "dataset-123"
    comment = "Excellent performance"
    tags = ["high_quality", "urgent"]
    mock_score = ModelScore(
        id=id,
        name=name,
        type=type.value,  # Assuming enum value handling
        value=value,
        step_id=stepId,
        generation_id=generationId,
        dataset_experiment_item_id=datasetExperimentItemId,
        comment=comment,
        tags=tags,
    )
    mock_create.return_value = mock_score

    result = await score_service.add_score(
        name, type, value, stepId, generationId, datasetExperimentItemId, comment, tags
    )

    assert isinstance(result, SchemaScore)
    assert result.id == mock_score.id
    assert result.name == mock_score.name
    assert result.type == mock_score.type
    assert result.value == mock_score.value
    assert result.stepId == mock_score.step_id
    assert result.generationId == mock_score.generation_id
    assert result.datasetExperimentItemId == mock_score.dataset_experiment_item_id
    assert result.comment == mock_score.comment
    assert result.tags == mock_score.tags
    mock_create.assert_awaited_once()


# Test for update_score
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.score.ScoreRepository.update",
    new_callable=AsyncMock,
)
async def test_update_score(mock_update, score_service):
    id = "score-123"
    name = "Updated Test Score"
    type = ScoreType.HUMAN  # Assuming ScoreType.HUMAN is the correct enum value
    value = 98.0
    stepId = "step-124"
    generationId = "gen-124"
    datasetExperimentItemId = "dataset-124"
    comment = "Updated excellent performance"
    tags = ["high_quality", "reviewed"]
    mock_score = ModelScore(
        id=id,
        name=name,
        type=type,
        value=value,
        step_id=stepId,
        generation_id=generationId,
        dataset_experiment_item_id=datasetExperimentItemId,
        comment=comment,
        tags=tags,
    )
    mock_update.return_value = mock_score

    result = await score_service.update_score(
        id,
        name,
        type,
        value,
        stepId,
        generationId,
        datasetExperimentItemId,
        comment,
        tags,
    )

    assert isinstance(result, SchemaScore)
    assert result.id == mock_score.id
    assert result.name == mock_score.name
    assert result.type == mock_score.type
    assert result.value == mock_score.value
    assert result.stepId == mock_score.step_id
    assert result.generationId == mock_score.generation_id
    assert result.datasetExperimentItemId == mock_score.dataset_experiment_item_id
    assert result.comment == mock_score.comment
    assert result.tags == mock_score.tags
    mock_update.assert_awaited_once_with(id, mock_score)


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.score.ScoreRepository.delete", new_callable=AsyncMock
)
async def test_delete_score(mock_delete, score_service):
    score_id = "score-123"
    mock_score = ModelScore(
        id=score_id,
        name="Test Score",
        type="AI",  # Assuming type is just a string in this model context
        value=88.5,
        step_id="step-123",
        generation_id="gen-123",
        dataset_experiment_item_id="dataset-123",
        comment="Well done",
        tags=["high_quality", "urgent"],
    )
    mock_delete.return_value = (
        mock_score  # Simulate successful deletion returning the score
    )

    result = await score_service.delete(score_id)

    assert isinstance(result, SchemaScore), "Result should be a SchemaScore instance"
    assert result.id == mock_score.id, "Deleted score ID should match the requested ID"
    assert result.name == mock_score.name, "Name of the deleted score should match"
    assert result.type == mock_score.type, "Type of the deleted score should match"
    assert result.value == mock_score.value, "Value of the deleted score should match"
    assert (
        result.stepId == mock_score.step_id
    ), "Step ID of the deleted score should match"
    assert (
        result.comment == mock_score.comment
    ), "Comment of the deleted score should match"
    assert result.tags == mock_score.tags, "Tags of the deleted score should match"
    mock_delete.assert_awaited_once_with(score_id)
