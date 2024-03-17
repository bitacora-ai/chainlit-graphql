from datetime import datetime
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from chainlit_graphql.api.v1.graphql.graphql_app import Query
from chainlit_graphql.api.v1.graphql.schema.thread import (
    PageInfo,
    StringListFilter,
    StringListOperators,
    ThreadConnection,
    ThreadFiltersInput,
    ThreadType,
)
from chainlit_graphql.api.v1.graphql.schema.participant import ParticipantType
from chainlit_graphql.service.apikey import ApikeyService
from chainlit_graphql.api.deps import IsValidApiKey


@pytest.mark.asyncio
@patch.object(ApikeyService, "validate_apikey", new_callable=AsyncMock)
async def test_valid_api_key(mock_validate_apikey):
    # Simulate validate_apikey returning True for a valid API key
    mock_validate_apikey.return_value = True

    # Mock Info context to simulate request with a valid API key in headers
    mock_info = MagicMock()
    mock_info.context = {"request": MagicMock()}
    mock_info.context["request"].headers.get.return_value = "valid-api-key"

    # Instantiate IsValidApiKey and test has_permission
    permission = IsValidApiKey()
    allowed = await permission.has_permission(None, mock_info)

    assert allowed is True
    mock_validate_apikey.assert_awaited_with("valid-api-key")


@pytest.mark.asyncio
@patch.object(ApikeyService, "validate_apikey", new_callable=AsyncMock)
async def test_invalid_api_key(mock_validate_apikey):
    # Simulate validate_apikey returning False for an invalid API key
    mock_validate_apikey.return_value = False

    # Mock Info context to simulate request with an invalid API key in headers
    mock_info = MagicMock()
    mock_info.context = {"request": MagicMock()}
    mock_info.context["request"].headers.get.return_value = "invalid-api-key"

    # Instantiate IsValidApiKey and test has_permission
    permission = IsValidApiKey()
    allowed = await permission.has_permission(None, mock_info)

    assert allowed is False
    mock_validate_apikey.assert_awaited_with("invalid-api-key")


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.participant.ParticipantService.get_by_id",
    new_callable=AsyncMock,
)
async def test_get_by_id_success(mock_get_by_id):
    participant_id = "participant-123"
    identifier = "identifier-123"
    metadata = '{"key":"value"}'
    created_at = datetime.now()
    mock_participant = ParticipantType(
        id=participant_id,
        identifier=identifier,
        createdAt=created_at,
        metadata=metadata,
    )
    mock_get_by_id.return_value = mock_participant

    query = Query()
    result = await query.get_by_id(id=participant_id, identifier=identifier)

    assert result == mock_participant
    mock_get_by_id.assert_awaited_once_with(participant_id, identifier)


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.thread.ThreadService.get_by_id", new_callable=AsyncMock
)
async def test_thread_detail_success(mock_get_by_id):
    thread_id = "thread-123"
    mock_thread = ThreadType(id=thread_id, name="Test Thread")
    mock_get_by_id.return_value = mock_thread

    query = Query()
    result = await query.threadDetail(id=thread_id)

    assert result == mock_thread
    mock_get_by_id.assert_awaited_once_with(thread_id)


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.participant.ParticipantService.get_by_id_or_identifier",
    new_callable=AsyncMock,
)
async def test_participant_success(mock_get_by_id_or_identifier):
    participant_id = "participant-123"
    identifier = "identifier-123"
    metadata = {"key": "value"}
    created_at = datetime.now()
    mock_participant = ParticipantType(
        id=participant_id,
        identifier=identifier,
        metadata=metadata,
        createdAt=created_at,
    )
    mock_get_by_id_or_identifier.return_value = mock_participant

    query = Query()
    result = await query.participant(id=participant_id, identifier=identifier)

    assert result == mock_participant
    mock_get_by_id_or_identifier.assert_awaited_once_with(participant_id, identifier)


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.service.thread.ThreadService.get_threads_paginated",
    new_callable=AsyncMock,
)
async def test_threads_success(mock_get_threads_paginated):
    after = "cursor1"
    before = "cursor2"
    first = 10
    filters = ThreadFiltersInput(
        participantsIdentifier=StringListFilter(
            operator=StringListOperators.in_.value, value=["sampleIdentifier"]
        )
    )
    mock_thread_connection = ThreadConnection(
        edges=[],
        page_info=PageInfo(
            has_next_page=True,
            has_previous_page=False,
            start_cursor="startCursor",
            end_cursor="endCursor",
        ),
    )
    mock_get_threads_paginated.return_value = mock_thread_connection

    query = Query()
    result = await query.threads(
        after=after, before=before, first=first, filters=filters
    )

    assert result == mock_thread_connection
    mock_get_threads_paginated.assert_awaited_once_with(
        after=after,
        before=before,
        first=first,
        filters=filters,
        last=None,
        projectId=None,
        skip=None,
        cursorAnchor=None,
    )
