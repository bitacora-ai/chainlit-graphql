from datetime import datetime, timezone
from chainlit_graphql.api.v1.graphql.schema.score import Score, ScoreType
import pytest
from unittest.mock import patch, AsyncMock

from chainlit_graphql.api.v1.graphql.graphql_app import Mutation
from chainlit_graphql.api.v1.graphql.schema.step import (
    AttachmentPayloadInput,
    GenerationPayloadInput,
    ScorePayloadInput,
    StepType,
    StepsType,
)
from chainlit_graphql.api.v1.graphql.schema.thread import ThreadType
from chainlit_graphql.service.thread import ThreadService
from chainlit_graphql.service.participant import ParticipantService
from chainlit_graphql.api.v1.graphql.schema.participant import ParticipantType


@pytest.mark.asyncio
@patch.object(ParticipantService, "add_participant", new_callable=AsyncMock)
async def test_create_participant_success(mock_add_participant):
    # Setup
    created_at = datetime.now()
    mock_participant = ParticipantType(
        id="123",
        identifier="test_participant",
        metadata={"key": "value"},
        createdAt=created_at,
    )
    mock_add_participant.return_value = mock_participant

    mutation = Mutation()

    # Exercise
    result = await mutation.createParticipant(
        identifier="test_participant", metadata='{"key": "value"}'
    )

    # Verify
    assert result == mock_participant
    mock_add_participant.assert_awaited_once_with(
        "test_participant", '{"key": "value"}'
    )


@pytest.mark.asyncio
@patch.object(ParticipantService, "delete", new_callable=AsyncMock)
async def test_delete_participant_success(mock_delete):
    participant_id = "participant-123"
    expected_message = "Successfully deleted data by id participant-123"
    mock_delete.return_value = expected_message

    mutation = Mutation()
    result = await mutation.deleteParticipant(id=participant_id)

    assert result == expected_message
    mock_delete.assert_awaited_once_with(participant_id)


@pytest.mark.asyncio
@patch.object(ThreadService, "delete", new_callable=AsyncMock)
async def test_delete_thread_success(mock_delete):
    thread_id = "thread-123"
    mock_thread = ThreadType(id=thread_id, name="Test Thread")
    mock_delete.return_value = mock_thread

    mutation = Mutation()
    result = await mutation.deleteThread(id=thread_id)

    assert result == mock_thread
    mock_delete.assert_awaited_once_with(thread_id)


@pytest.mark.asyncio
@patch.object(ParticipantService, "update", new_callable=AsyncMock)
async def test_update_participant_success(mock_update):
    participant_id = "participant-123"
    identifier = "new_identifier"
    metadata = '{"key":"value"}'
    created_at = datetime.now()
    mock_participant = ParticipantType(
        id=participant_id,
        identifier=identifier,
        metadata=metadata,
        createdAt=created_at,
    )
    mock_update.return_value = mock_participant

    mutation = Mutation()
    result = await mutation.updateParticipant(
        id=participant_id, identifier=identifier, metadata=metadata
    )

    assert result == mock_participant
    mock_update.assert_awaited_once_with(participant_id, identifier, metadata)


@pytest.mark.asyncio
@patch.object(ThreadService, "upsert_thread", new_callable=AsyncMock)
async def test_upsert_thread_success(mock_upsert):
    thread_id = "thread-123"
    name = "New Thread"
    metadata = '{"environment":"prod"}'
    environment = "prod"
    tags = ["urgent", "review"]
    mock_thread = ThreadType(
        id=thread_id, name=name, metadata=metadata, environment=environment, tags=tags
    )
    mock_upsert.return_value = mock_thread

    mutation = Mutation()
    result = await mutation.upsertThread(
        id=thread_id,
        name=name,
        metadata=metadata,
        participantId="participant-123",
        environment=environment,
        tags=tags,
    )

    assert result == mock_thread
    # Ensure correct arguments, including using `participantId` as a keyword argument, are passed
    mock_upsert.assert_awaited_once_with(
        id=thread_id,
        name=name,
        metadata=metadata,
        participantId="participant-123",
        environment=environment,
        tags=tags,
    )


@pytest.mark.asyncio
@patch("chainlit_graphql.service.step.StepService.upsert", new_callable=AsyncMock)
async def test_ingest_step_success(mock_upsert_step):
    step_id = "step-1"
    thread_id = "thread-123"
    start_time = datetime.now(timezone.utc)
    end_time = datetime.now(timezone.utc)
    step_type = StepType.user_message
    error = None
    input_data = '{"key": "input value"}'
    output_data = '{"key": "output value"}'
    metadata = '{"key": "metadata value"}'
    parent_id = "parent-1"
    name = "Test Step"
    tags = ["tag1", "tag2"] 
    generation = GenerationPayloadInput(type="test-type")
    attachments = [AttachmentPayloadInput(id="attachment-1")]
    scores = [
        ScorePayloadInput(
            comment="very good", type="HUMAN", name="the name", value=0.99
        )
    ]

    mock_step = StepsType(
        id=step_id,
        thread_id=thread_id,
        start_time=start_time,
        end_time=end_time,
        type=step_type,
        error=error,
        input=input_data,
        output=output_data,
        metadata=metadata,
        parent_id=parent_id,
        name=name,
        createdAt=datetime.now(timezone.utc), 
    )
    mock_upsert_step.return_value = mock_step

    mutation = Mutation()
    result = await mutation.ingestStep(
        id=step_id,
        threadId=thread_id,
        startTime=start_time,
        endTime=end_time,
        type=step_type,
        error=error,
        input=input_data,
        output=output_data,
        metadata=metadata,
        parentId=parent_id,
        name=name,
        tags=tags, 
        generation=generation,
        attachments=attachments,
        scores=scores,
    )

    assert result == mock_step
    mock_upsert_step.assert_awaited_once_with(
        step_id,
        thread_id,
        start_time,
        end_time,
        step_type,
        error,
        input_data,
        output_data,
        metadata,
        parent_id,
        name,
        tags,  
        scores,
        generation,
        attachments,
    )


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.thread.ThreadService.add_thread", new_callable=AsyncMock
)
async def test_create_thread_success(mock_add_thread):
    name = "New Thread"
    metadata = '{"environment": "prod"}'
    participant_id = "participant-123"
    environment = "prod"
    tags = ["urgent", "review"]

    mock_thread = ThreadType(id="thread-123", name=name)
    mock_add_thread.return_value = mock_thread

    mutation = Mutation()
    result = await mutation.createThread(
        name=name,
        metadata=metadata,
        participantId=participant_id,
        environment=environment,
        tags=tags,
    )

    assert result == mock_thread
    mock_add_thread.assert_awaited_once_with(
        name,
        metadata,
        participant_id,
        environment,
        tags,
    )


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.score.ScoreService.add_score",
    new_callable=AsyncMock,
)
async def test_create_score_success(mock_add_score):
    id = "score-123"
    name = "Test Score"
    type = ScoreType.AI
    value = 99.5
    step_id = "step-456"
    generation_id = "gen-789"
    dataset_experiment_item_id = "dataset-123"
    comment = "Outstanding performance"
    tags = ["urgent", "review"]

    mock_score = Score(
        id=id,
        name=name,
        type=type,
        value=value,
        stepId=step_id,
        generationId=generation_id,
        datasetExperimentItemId=dataset_experiment_item_id,
        comment=comment,
        tags=tags,
    )
    mock_add_score.return_value = mock_score

    mutation = Mutation()
    result = await mutation.createScore(
        name=name,
        type=type,
        value=value,
        stepId=step_id,
        generationId=generation_id,
        datasetExperimentItemId=dataset_experiment_item_id,
        comment=comment,
        tags=tags,
    )

    assert result == mock_score
    mock_add_score.assert_awaited_once_with(
        name=name,
        type=type,
        value=value,
        stepId=step_id,
        generationId=generation_id,
        datasetExperimentItemId=dataset_experiment_item_id,
        comment=comment,
        tags=tags,
    )


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.score.ScoreService.update_score",
    new_callable=AsyncMock,
)
async def test_update_score_success(mock_update_score):
    id = "score-123"
    name = "Updated Test Score"
    type = ScoreType.HUMAN
    value = 95.0
    step_id = "step-456"
    generation_id = "gen-789"
    dataset_experiment_item_id = "dataset-123"
    comment = "Improved performance"
    tags = ["high_priority", "reviewed"]

    mock_score = Score(
        id=id,
        name=name,
        type=type,
        value=value,
        stepId=step_id,
        generationId=generation_id,
        datasetExperimentItemId=dataset_experiment_item_id,
        comment=comment,
        tags=tags,
    )
    mock_update_score.return_value = mock_score

    mutation = Mutation()
    result = await mutation.updateScore(
        id=id,
        name=name,
        type=type,
        value=value,
        stepId=step_id,
        generationId=generation_id,
        datasetExperimentItemId=dataset_experiment_item_id,
        comment=comment,
        tags=tags,
    )

    assert result == mock_score
    mock_update_score.assert_awaited_once_with(
        id=id,
        name=name,
        type=type,
        value=value,
        stepId=step_id,
        generationId=generation_id,
        datasetExperimentItemId=dataset_experiment_item_id,
        comment=comment,
        tags=tags,
    )


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.score.ScoreService.delete",
    new_callable=AsyncMock,
)
async def test_delete_score_success(mock_delete_score):
    score_id = "score-123"
    mock_score = Score(
        id=score_id,
        name="Test Score",
        type=ScoreType.AI,
        value=99.5,
        stepId="step-456",
        generationId="gen-789",
        datasetExperimentItemId="dataset-123",
        comment="Outstanding performance",
        tags=["urgent", "review"],
    )
    mock_delete_score.return_value = mock_score

    mutation = Mutation()
    result = await mutation.deleteScore(id=score_id)

    assert result == mock_score, "Mutation should return the deleted Score object"
    mock_delete_score.assert_awaited_once_with(score_id)
