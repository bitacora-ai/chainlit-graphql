import pytest
import json
from unittest.mock import patch, AsyncMock
from chainlit_graphql.service.thread import ThreadService
from chainlit_graphql.repository.thread import thread_repo
from chainlit_graphql.api.v1.graphql.schema.thread import ThreadConnection, ThreadType


@pytest.fixture
def thread_service():
    return ThreadService(thread_repo)


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.thread.thread_repo.upsert_thread",
    new_callable=AsyncMock,
)
async def test_add_thread(mock_upsert_thread, thread_service):
    # Prepare mock return value
    mock_thread = ThreadType(id="123", name="Test Thread")
    mock_upsert_thread.return_value = mock_thread

    # Call the service method
    result = await thread_service.add_thread(
        name="Test Thread",
        metadata=json.dumps({"key": "value"}),  # Assuming metadata is a JSON string
        participantId="participant-1",
        environment="test-environment",
        tags=["tag1", "tag2"],
    )

    # Assertions
    assert result == mock_thread
    mock_upsert_thread.assert_called_once_with(
        "Test Thread",
        {"key": "value"},  # The service is expected to load the JSON
        "participant-1",
        "test-environment",
        json.dumps(
            ["tag1", "tag2"]
        ),  # The service might convert the list to JSON string
    )


@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.thread.thread_repo.get_paginated_threads",
    new_callable=AsyncMock,
)
async def test_get_threads_paginated(mock_get_paginated_threads, thread_service):
    mock_connection = ThreadConnection(page_info=None, edges=[])
    mock_get_paginated_threads.return_value = mock_connection

    result = await thread_service.get_threads_paginated()
    assert result == mock_connection
    mock_get_paginated_threads.assert_called_once()


# Test for get_by_id
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.thread.thread_repo._get_by_id_with_session",
    new_callable=AsyncMock,
)
async def test_get_by_id(mock_get_by_id, thread_service):
    mock_thread = ThreadType(id="123", name="Test Thread")
    mock_get_by_id.return_value = mock_thread

    result = await thread_service.get_by_id("123")
    assert result == mock_thread
    mock_get_by_id.assert_called_once_with("123")


# Test for upsert_thread
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.thread.thread_repo.upsert_thread",
    new_callable=AsyncMock,
)
async def test_upsert_thread(mock_upsert_thread, thread_service):
    mock_thread = ThreadType(id="123", name="Test Thread")
    mock_upsert_thread.return_value = mock_thread

    result = await thread_service.upsert_thread(
        id="123",
        name="Test Thread",
        tags=["tag1", "tag2"],
        metadata=json.dumps({"key": "value"}),
    )
    assert result == mock_thread
    mock_upsert_thread.assert_called_once_with(
        "123",
        "Test Thread",
        ["tag1", "tag2"],
        json.dumps({"key": "value"}),
        None,
        None,
    )


# Test for delete
@pytest.mark.asyncio
@patch("chainlit_graphql.repository.thread.thread_repo.delete", new_callable=AsyncMock)
async def test_delete(mock_delete, thread_service):
    mock_thread = ThreadType(id="123", name="Deleted Thread")
    mock_delete.return_value = mock_thread

    result = await thread_service.delete("123")
    assert result == mock_thread
    mock_delete.assert_called_once_with("123")
