import pytest
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.participant import participant_repo
from chainlit_graphql.model.participant import Participant
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_create_participant(prepare_db):
    async with db.SessionLocal():
        participant_data = Participant(
            id="participant-1",
            identifier="identifier-1",
            createdAt=datetime.now(timezone.utc),
        )
        created_participant = await participant_repo.create(participant_data)
        assert created_participant is not None
        assert created_participant.id == "participant-1"


@pytest.mark.asyncio
async def test_get_by_id(prepare_db):
    async with db.SessionLocal() as session:
        participant_id = "participant-2"
        identifier = "identifier-2"
        # Make createdAt timezone-aware, explicitly setting it to UTC
        createdAt = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        participant_data = Participant(
            id=participant_id, identifier=identifier, createdAt=createdAt
        )
        session.add(participant_data)
        await session.commit()

        result = await participant_repo.get_by_id(participant_id=participant_id)
        assert result is not None
        assert result.id == participant_id
        assert result.identifier == identifier
        # When comparing, ensure createdAt is compared with timezone awareness
        assert result.createdAt == createdAt


@pytest.mark.asyncio
async def test_update_participant(prepare_db):
    async with db.SessionLocal() as session:
        participant_id = "participant-3"
        participant_data = Participant(
            id=participant_id,
            identifier="identifier-3",
            createdAt=datetime.now(timezone.utc),
        )
        session.add(participant_data)
        await session.commit()

        participant_data.meta_data = {"key": "updated value"}
        updated_participant = await participant_repo.update(participant_data)
        assert updated_participant is not None
        assert updated_participant.meta_data == {"key": "updated value"}


@pytest.mark.asyncio
async def test_delete_participant(prepare_db):
    async with db.SessionLocal() as session:
        participant_id = "participant-4"
        participant_data = Participant(
            id=participant_id,
            identifier="identifier-4",
            createdAt=datetime.now(timezone.utc),
        )
        session.add(participant_data)
        await session.commit()

        # Call delete method - Ensure this operates within its own session context as defined in the method
        await participant_repo.delete(participant_id)

        # To check deletion, a new session context is needed to reflect the committed state
        async with db.SessionLocal() as session:
            deleted_participant = await session.get(Participant, participant_id)
            assert deleted_participant is None


@pytest.mark.asyncio
async def test_get_by_identifier(prepare_db):
    async with db.SessionLocal() as session:
        identifier = "identifier-5"
        participant_data = Participant(
            id="participant-5",
            identifier=identifier,
            createdAt=datetime.now(timezone.utc),
        )
        session.add(participant_data)
        await session.commit()

        result = await participant_repo.get_by_identifier(identifier=identifier)
        assert result is not None
        assert result.identifier == identifier


@pytest.mark.asyncio
async def test_get_by_id_or_identifier(prepare_db):
    async with db.SessionLocal() as session:
        participant_id = "participant-6"
        identifier = "identifier-6"
        participant_data = Participant(
            id=participant_id,
            identifier=identifier,
            createdAt=datetime.now(timezone.utc),
        )
        session.add(participant_data)
        await session.commit()

        result_by_id = await participant_repo.get_by_id_or_identifier(id=participant_id)
        assert result_by_id is not None
        assert result_by_id.id == participant_id

        result_by_identifier = await participant_repo.get_by_id_or_identifier(
            identifier=identifier
        )
        assert result_by_identifier is not None
        assert result_by_identifier.identifier == identifier
