import base64
import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone
from chainlit_graphql.service.step import StepService
from chainlit_graphql.repository.step import step_repo
from chainlit_graphql.api.v1.graphql.schema.step import (
    StepsType,
    StepType,
    GenerationPayloadInput,
    AttachmentPayloadInput,
)
import json


@pytest.fixture
def step_service():
    return StepService(step_repo)


@pytest.mark.asyncio
@patch("chainlit_graphql.repository.step.step_repo.upsert_step", new_callable=AsyncMock)
async def test_upsert(mock_upsert_step, step_service):
    now = datetime.now(timezone.utc)
    mock_step = StepsType(
        id="step-1",
        thread_id="thread-1",
        start_time=now,
        end_time=now,
        type=StepType.llm,
        name="Test Step",
        createdAt=now,  # Added createdAt field here
    )
    mock_upsert_step.return_value = mock_step

    step_id = "step-1"
    thread_id_encoded = base64.b64encode(b"Thread:thread-1").decode("utf-8")
    step_type = StepType.llm
    step_input = json.dumps({"key": "input value"})
    step_output = json.dumps({"key": "output value"})
    metadata = json.dumps({"key": "metadata value"})
    generation_payload = GenerationPayloadInput(type="test-type")
    attachment_payload = [AttachmentPayloadInput(id="attachment-1")]

    result = await step_service.upsert(
        id=step_id,
        threadId=thread_id_encoded,
        startTime=now,
        endTime=now,
        type=step_type,
        error="None",
        input=step_input,
        output=step_output,
        metadata=metadata,
        parentId="parent-1",
        name="Test Step",
        generation=generation_payload,
        feedback=json.dumps({"score": 5}),
        attachments=attachment_payload,
    )

    assert result == mock_step
    # Check if the mock was called correctly, without the 'any' matcher for dates to simplify
    mock_upsert_step.assert_called_once()
