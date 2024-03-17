import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.future import select
from chainlit_graphql.api.v1.graphql.schema.step import StepsType
from chainlit_graphql.api.v1.graphql.schema.participant import ParticipantType
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.thread import thread_repo
from chainlit_graphql.model import Thread, Participant, Step
from chainlit_graphql.api.v1.graphql.schema.thread import (
    ThreadFiltersInput,
    StringListFilter,
    StringListOperators,
    ThreadType,
)
from datetime import datetime, timedelta, timezone
import base64


@pytest.mark.asyncio
async def test_get_paginated_threads(prepare_db):
    # Prepare a session and repository instance
    async with db.SessionLocal() as session:

        # Mock data
        participant = Participant(id="1", identifier="participant-123")
        step = Step(id="1", type="Step 1")
        thread = Thread(
            id="1",
            participant=participant,
            steps=[step],
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        # Add mock data to the database
        session.add(participant)
        session.add(step)
        session.add(thread)
        await session.commit()

        # Mock ThreadFiltersInput
        filters = ThreadFiltersInput(
            participantsIdentifier=StringListFilter(
                operator=StringListOperators.in_, value=["participant-123"]
            )
        )

        # Call the method under test
        threads_connection = await thread_repo.get_paginated_threads(
            filters=filters, first=1
        )

        # Assertions
        assert threads_connection.total_count == 1
        assert len(threads_connection.edges) == 1
        first_edge = threads_connection.edges[0]

        # Updated assertions to reflect actual structure and attributes
        # Assuming `ThreadType` and `ParticipantType` have `id` fields as a common attribute
        assert hasattr(first_edge.node, "id"), "ThreadType does not have 'id' attribute"
        assert first_edge.node.id == str(thread.id), "Thread ID does not match"

        # If ParticipantType maps directly to Participant and uses 'identifier' to match 'participant-123'
        assert hasattr(
            first_edge.node, "participant"
        ), "ThreadType does not have 'participant' attribute"
        assert (
            first_edge.node.participant.identifier == participant.identifier
        ), "Participant identifier does not match"

        # Decode the cursor and ensure it matches the thread ID
        decoded_cursor = base64.b64decode(first_edge.cursor).decode()
        assert decoded_cursor == f"Thread:{thread.id}"


@pytest.mark.asyncio
async def test_upsert_thread(prepare_db):
    # Prepare a session for database operations
    async with db.SessionLocal() as session:
        # First, create a participant to satisfy the foreign key constraint
        participant_id = "participant-123"
        participant = Participant(id=participant_id, identifier="some-identifier")
        session.add(participant)
        await session.commit()

        # Setup mock thread data
        thread_id = "1"
        name = "Test Thread"
        tags = ["tag1", "tag2"]
        metadata = {"key": "value"}
        participantId = participant_id  # Use the created participant ID
        environment = "test"

        # Encode the thread ID in base64 to simulate an encoded ID input
        encoded_thread_id = base64.b64encode(f"Thread:{thread_id}".encode()).decode()

        # Call the method under test with encoded ID and serialized tags
        thread_type = await thread_repo.upsert_thread(
            id=encoded_thread_id,
            name=name,
            tags=tags,
            metadata=metadata,
            participantId=participantId,
            environment=environment,
        )

        # Assertions to ensure the thread was correctly inserted/updated
        assert thread_type is not None, "ThreadType object should not be None"
        assert thread_type.name == name, "Thread name does not match"
        assert (
            thread_type.environment == environment
        ), "Thread environment does not match"
        assert thread_type.tags == tags, "Thread tags do not match"
        assert thread_type.metadata == metadata, "Thread metadata does not match"
        # If there's a specific way to assert the participant, add assertions for participantId here

        # Fetch the thread directly from the database to ensure it was correctly inserted/updated
        db_thread = await thread_repo.get_by_id(thread_id, session)
        assert db_thread is not None, "Thread was not found in the database"
        assert db_thread.name == name, "Database thread name does not match"
        assert (
            db_thread.environment == environment
        ), "Database thread environment does not match"
        assert db_thread.tags == tags, "Database thread tags do not match"
        assert (
            db_thread.meta_data == metadata
        ), "Database thread metadata does not match"


@pytest.mark.asyncio
async def test_update_thread(prepare_db):
    async with db.SessionLocal() as session:
        # First, insert a thread and a participant to satisfy the foreign key constraint
        participant_id = "participant-123"
        participant = Participant(id=participant_id, identifier="some-identifier")
        original_thread_id = "original_thread_id"
        original_thread = Thread(
            id=original_thread_id,
            name="Original Thread",
            tags=["original_tag1", "original_tag2"],
            meta_data={"originalKey": "originalValue"},
            participant_id=participant_id,
            environment="original_environment",
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(participant)
        session.add(original_thread)
        await session.commit()

        # New data for updating the existing thread
        new_name = "Updated Test Thread"
        new_tags = ["updated_tag1", "updated_tag2"]
        new_metadata = {"updatedKey": "updatedValue"}
        new_environment = "updated_test"

        # Encode the thread ID in base64 to simulate an encoded ID input
        encoded_thread_id = base64.b64encode(
            f"Thread:{original_thread_id}".encode()
        ).decode()

        # Call the method under test with new data for the existing thread
        updated_thread_type = await thread_repo.upsert_thread(
            id=encoded_thread_id,
            name=new_name,
            tags=new_tags,
            metadata=new_metadata,
            participantId=participant_id,  # Use the existing participant ID
            environment=new_environment,
        )

        expected_metadata = {
            "originalKey": "originalValue",
            "updatedKey": "updatedValue",
        }

        # Assertions to ensure the thread was correctly updated
        assert (
            updated_thread_type is not None
        ), "ThreadType object should not be None after update"
        assert (
            updated_thread_type.name == new_name
        ), "Thread name did not update correctly"
        assert (
            updated_thread_type.environment == new_environment
        ), "Thread environment did not update correctly"
        assert (
            updated_thread_type.tags == new_tags
        ), "Thread tags did not update correctly"
        assert (
            updated_thread_type.metadata == expected_metadata
        ), "Thread metadata did not update correctly"

        # Fetch the thread directly from the database to ensure it was correctly updated
        session.expire_all()
        db_thread = await thread_repo.get_by_id(original_thread_id, session)
        print(original_thread_id)
        assert (
            db_thread is not None
        ), "Thread was not found in the database after update"
        assert (
            db_thread.name == new_name
        ), "Database thread name did not update correctly"
        assert (
            db_thread.environment == new_environment
        ), "Database thread environment did not update correctly"
        assert (
            db_thread.tags == new_tags
        ), "Database thread tags did not update correctly"
        assert (
            db_thread.meta_data == expected_metadata
        ), "Database thread metadata did not update correctly"


@pytest.mark.asyncio
async def test_get_thread_by_id_with_steps_and_participant(prepare_db):
    async with db.SessionLocal() as session:
        # Use datetime.now(timezone.utc).replace(tzinfo=None) to get the current UTC time without setting timezone
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)

        # Adjusted to use utc_now for createdAt without timezone info
        participant = Participant(
            id="participant-123", identifier="participant-identifier", createdAt=utc_now
        )
        thread = Thread(
            id="thread-1",
            name="Test Thread",
            participant=participant,
            createdAt=utc_now,
        )
        step1 = Step(id="step-1", thread=thread, createdAt=utc_now - timedelta(days=1))
        step2 = Step(id="step-2", thread=thread, createdAt=utc_now)

        session.add_all([participant, thread, step1, step2])
        await session.commit()

        fetched_thread = await thread_repo.get_by_id("thread-1", session)

        assert fetched_thread is not None, "Thread not found by ID"
        assert fetched_thread.id == "thread-1", "Fetched thread ID mismatch"
        assert (
            fetched_thread.participant.id == "participant-123"
        ), "Fetched thread participant ID mismatch"
        assert len(fetched_thread.steps) == 2, "Incorrect number of steps fetched"
        assert (
            fetched_thread.steps[0].id == "step-1"
        ), "Steps are not correctly ordered by 'createdAt'"
        assert (
            fetched_thread.steps[1].id == "step-2"
        ), "Steps are not correctly ordered by 'createdAt'"


@pytest.mark.asyncio
async def test_get_by_id_with_session(prepare_db):
    # Insert test data using the session from your fixture
    async with db.SessionLocal() as session:
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)

        # Setup test data
        participant = Participant(
            id="participant-123", identifier="participant-identifier", createdAt=utc_now
        )
        thread = Thread(
            id="thread-1",
            name="Test Thread",
            participant=participant,
            createdAt=utc_now,
        )
        step1 = Step(id="step-1", thread=thread, createdAt=utc_now - timedelta(days=1))
        step2 = Step(id="step-2", thread=thread, createdAt=utc_now)

        session.add_all([participant, thread, step1, step2])
        await session.commit()

    # Fetch the inserted Thread by ID using the method under test
    fetched_thread = await thread_repo._get_by_id_with_session("thread-1")

    # Assertions to verify that the fetched data matches the inserted data
    assert fetched_thread is not None, "Thread not found by ID"
    assert fetched_thread.id == "thread-1", "Fetched thread ID mismatch"
    assert (
        fetched_thread.participant_id == "participant-123"
    ), "Fetched thread participant ID mismatch"
    assert len(fetched_thread.steps) == 2, "Incorrect number of steps fetched"


@pytest.mark.asyncio
async def test_delete_thread(prepare_db):
    # Insert test data using the session from your fixture
    async with db.SessionLocal() as session:
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)

        # Setup test data: Participant and Thread entities
        participant = Participant(
            id="participant-123", identifier="participant-identifier", createdAt=utc_now
        )
        thread = Thread(
            id="thread-1",
            name="Test Thread",
            participant=participant,
            createdAt=utc_now,
        )

        # Add and commit data to the session
        session.add_all([participant, thread])
        await session.commit()

    # Now, try to delete the inserted Thread by its ID
    deleted_thread = await thread_repo.delete("thread-1")

    # Assertions to verify the deletion was successful
    assert (
        deleted_thread is not None
    ), "No ThreadType object was returned after deletion"
    assert deleted_thread.id == "thread-1", "The deleted thread ID does not match"

    # Further verify the thread is actually deleted from the database
    async with db.SessionLocal() as session:
        # Attempt to fetch the deleted thread
        result = await session.execute(select(Thread).filter_by(id="thread-1"))
        thread_after_deletion = result.scalars().first()

        assert thread_after_deletion is None, "Thread was not deleted from the database"


@pytest.mark.asyncio
async def test_map_to_thread_type():
    # Setup mock data for Thread, Steps, and Participant
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    mock_participant = Participant(
        id="participant-1", identifier="participant-identifier", createdAt=utc_now
    )
    mock_step1 = Step(id="step-1", thread_id="thread-1", createdAt=utc_now)
    mock_step2 = Step(id="step-2", thread_id="thread-1", createdAt=utc_now)
    mock_thread = Thread(
        id="thread-1",
        name="Test Thread",
        meta_data={"key": "value"},
        environment="Test Environment",
        tags=["tag1", "tag2"],
        createdAt=utc_now,
        participant_id="participant-1",
        participant=mock_participant,
        steps=[mock_step1, mock_step2],
    )

    # Mock the async map_step_to_stepstype method
    mock_steps_type1 = StepsType(
        id="step-1", thread_id="thread-1", createdAt=utc_now, name="Step 1"
    )
    mock_steps_type2 = StepsType(
        id="step-2", thread_id="thread-1", createdAt=utc_now, name="Step 2"
    )
    with patch(
        "chainlit_graphql.core.mappers.MapperUtility.map_step_to_stepstype",
        new_callable=AsyncMock,
    ) as mocked_mapper:
        mocked_mapper.side_effect = [mock_steps_type1, mock_steps_type2]

        # Call the static method under test
        result = await thread_repo.map_to_thread_type(mock_thread)

        # Verify the overall structure of the result
        assert isinstance(result, ThreadType)
        assert result.id == mock_thread.id
        assert result.name == mock_thread.name
        assert result.metadata == mock_thread.meta_data
        assert result.environment == mock_thread.environment
        assert result.tags == mock_thread.tags
        assert result.createdAt == mock_thread.createdAt
        assert result.participant_id == mock_thread.participant_id
        assert len(result.steps) == 2
        assert all(isinstance(step, StepsType) for step in result.steps)

        # Verify mapping of the participant
        assert isinstance(result.participant, ParticipantType)
        assert result.participant.id == mock_participant.id
        assert result.participant.identifier == mock_participant.identifier
        assert result.participant.createdAt == mock_participant.createdAt

        # Ensure the steps mapping function was called correctly
        mocked_mapper.assert_called()
        assert mocked_mapper.call_count == 2
