from chainlit_graphql.model.participant import Participant
from chainlit_graphql.repository.participant import ParticipantRepository
from chainlit_graphql.api.v1.graphql.schema.participant import ParticipantType
from typing import Optional
from chainlit_graphql.api.v1.graphql.scalars.json_scalar import Json


class ParticipantService:
    def __init__(self, participant_repository: ParticipantRepository):
        self.participant_repository = participant_repository

    async def add_participant(
        self, identifier: str, metadata: Optional[Json]
    ) -> ParticipantType:
        existing_participant = await self.participant_repository.get_by_identifier(
            identifier
        )
        if existing_participant:
            raise ValueError("Identifier is already registered!")
        created_participant = await self.participant_repository.create(
            Participant(
                identifier=identifier,
                meta_data=metadata,
            )
        )

        return ParticipantType(
            id=created_participant.id,
            identifier=created_participant.identifier,
            metadata=created_participant.meta_data,
            createdAt=created_participant.createdAt,
        )

    async def get_by_id(self, id: Optional[str], identifier: Optional[str]):
        participant = await self.participant_repository.get_by_id(id, identifier)
        return ParticipantType(
            id=participant.id or "",
            identifier=participant.identifier or "",
            metadata=participant.meta_data or "{}",
            createdAt=participant.createdAt or "",
        )

    async def delete(self, id: str):
        await self.participant_repository.delete(id)
        return f"Successfully deleted data by id {id}"

    async def update(
        self, id: str, identifier: Optional[str], metadata: Optional[Json]
    ) -> ParticipantType:

        # Convert participant_data to Participant model instance
        participant_to_update = Participant(
            id=id, identifier=identifier, meta_data=metadata
        )

        # Pass this participant to ParticipantRepository for updating
        updated_participant = await self.participant_repository.update(
            participant_to_update
        )

        if updated_participant:
            # Return a ParticipantType object
            return ParticipantType(
                id=updated_participant.id,
                identifier=updated_participant.identifier,
                metadata=updated_participant.meta_data,
                createdAt=updated_participant.createdAt,
            )
        else:
            raise ValueError(f"Participant with id {id} not found")

    async def get_by_id_or_identifier(
        self, id: Optional[str] = None, identifier: Optional[str] = None
    ) -> Optional[Participant]:

        participant = await self.participant_repository.get_by_id_or_identifier(
            id, identifier
        )

        if participant:
            # Return a ParticipantType object
            return ParticipantType(
                id=participant.id,
                identifier=participant.identifier,
                metadata=participant.meta_data,
                createdAt=participant.createdAt,
            )

        return None
