import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from chainlit_graphql.service.participant import ParticipantService
from chainlit_graphql.repository.participant import participant_repo
from chainlit_graphql.model.participant import Participant
from chainlit_graphql.api.v1.graphql.schema.participant import ParticipantType
import json


@pytest.fixture
def participant_service():
    return ParticipantService(participant_repo)


# Test for add_participant
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.participant.ParticipantRepository.get_by_identifier",
    new_callable=AsyncMock,
)
@patch(
    "chainlit_graphql.repository.participant.ParticipantRepository.create",
    new_callable=AsyncMock,
)
async def test_add_participant(
    mock_create, mock_get_by_identifier, participant_service
):
    identifier = "unique_identifier"
    metadata = json.dumps({"key": "value"})
    mock_get_by_identifier.return_value = None
    mock_participant = Participant(
        id="123", identifier=identifier, meta_data=metadata, createdAt=datetime.now()
    )
    mock_create.return_value = mock_participant

    result = await participant_service.add_participant(identifier, metadata)
    assert isinstance(result, ParticipantType)
    assert result.identifier == identifier
    mock_get_by_identifier.assert_awaited_once_with(identifier)
    mock_create.assert_awaited_once()


# Test for get_by_id
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.participant.ParticipantRepository.get_by_id",
    new_callable=AsyncMock,
)
async def test_get_by_id(mock_get_by_id, participant_service):
    participant_id = "123"
    identifier = "participant123"
    metadata = json.dumps({"key": "value"})
    createdAt = datetime.now()
    mock_participant = Participant(
        id=participant_id,
        identifier=identifier,
        meta_data=metadata,
        createdAt=createdAt,
    )
    mock_get_by_id.return_value = mock_participant

    result = await participant_service.get_by_id(participant_id, None)
    assert isinstance(result, ParticipantType)
    assert result.id == participant_id
    mock_get_by_id.assert_awaited_once_with(participant_id, None)


# Test for delete
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.participant.ParticipantRepository.delete",
    new_callable=AsyncMock,
)
async def test_delete(mock_delete, participant_service):
    participant_id = "123"
    mock_delete.return_value = None

    result = await participant_service.delete(participant_id)
    assert result == f"Successfully deleted data by id {participant_id}"
    mock_delete.assert_awaited_once_with(participant_id)


# Test for update
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.participant.ParticipantRepository.update",
    new_callable=AsyncMock,
)
async def test_update(mock_update, participant_service):
    participant_id = "123"
    identifier = "participant123"
    metadata = json.dumps({"key": "value"})
    createdAt = datetime.now()
    mock_participant = Participant(
        id=participant_id,
        identifier=identifier,
        meta_data=metadata,
        createdAt=createdAt,
    )
    mock_update.return_value = mock_participant

    result = await participant_service.update(participant_id, identifier, metadata)
    assert isinstance(result, ParticipantType)
    assert result.id == participant_id
    mock_update.assert_awaited_once()


# Test for get_by_id_or_identifier
@pytest.mark.asyncio
@patch(
    "chainlit_graphql.repository.participant.ParticipantRepository.get_by_id_or_identifier",
    new_callable=AsyncMock,
)
async def test_get_by_id_or_identifier(
    mock_get_by_id_or_identifier, participant_service
):
    participant_id = "123"
    identifier = "participant123"
    metadata = json.dumps({"key": "value"})
    createdAt = datetime.now()
    mock_participant = Participant(
        id=participant_id,
        identifier=identifier,
        meta_data=metadata,
        createdAt=createdAt,
    )
    mock_get_by_id_or_identifier.return_value = mock_participant

    result = await participant_service.get_by_id_or_identifier(participant_id, None)
    assert isinstance(result, ParticipantType)
    assert result.id == participant_id
    mock_get_by_id_or_identifier.assert_awaited_once_with(participant_id, None)
