from chainlit_graphql.model.participant import Participant
from chainlit_graphql.api.v1.graphql.schema.participant import ParticipantType
from chainlit_graphql.db.database import db
from sqlalchemy.sql import select
from sqlalchemy import delete as sql_delete, or_
from typing import Optional


class ParticipantRepository:

    @staticmethod
    async def create(participant_data: Participant) -> Participant:
        async for session in db.get_db():
            async with session.begin():
                # Add the new participant to the session
                session.add(participant_data)

                # Flush the session to ensure the participant is persisted
                await session.flush()

                # Refresh the instance to get any updated attributes from the database
                await session.refresh(participant_data)

                # Commit the transaction
                await session.commit()

        # Return the newly created participant
        return participant_data

    @staticmethod
    async def get_by_id(
        participant_id: Optional[str] = None, identifier: Optional[str] = None
    ) -> Optional[ParticipantType]:
        # Return None or raise an exception if both participant_id and identifier are None
        if participant_id is None and identifier is None:
            return None  # or raise ValueError("Both participant_id and identifier cannot be None.")

        async for session in db.get_db():
            # Construct the query based on provided parameters
            stmt = select(Participant)
            if participant_id is not None:
                stmt = stmt.where(Participant.id == participant_id)
            if identifier is not None:
                stmt = stmt.where(Participant.identifier == identifier)

            # Execute the query
            result = await session.execute(stmt)
            participant = result.scalars().first()

            # Return the ParticipantType if a participant is found
            if participant:
                return ParticipantType(
                    id=participant.id,
                    identifier=participant.identifier,
                    metadata=participant.meta_data,
                    createdAt=participant.createdAt,
                )

            # Return None if no participant is found
            return None

    @staticmethod
    async def update(participant: Participant) -> Optional[Participant]:
        async for session in db.get_db():
            async with session.begin():
                # Retrieve the existing participant
                existing_participant = await session.get(Participant, participant.id)

                # Update the participant if it exists
                if existing_participant:
                    if participant.meta_data is not None:
                        existing_participant.meta_data = participant.meta_data
                    if participant.identifier is not None:
                        existing_participant.identifier = participant.identifier

                    # Flush the session to ensure the participant is updated
                    await session.flush()

                    # Refresh the instance to get any updated attributes from the database
                    await session.refresh(existing_participant)

                    # Commit the transaction
                    await session.commit()
                    return existing_participant
                else:
                    return None

    @staticmethod
    async def delete(participant_id: str):
        async for session in db.get_db():
            async with session.begin():
                query = sql_delete(Participant).where(Participant.id == participant_id)
                await session.execute(query)

    @staticmethod
    async def get_by_identifier(identifier: str) -> Optional[ParticipantType]:
        async for session in db.get_db():
            stmt = select(Participant).where(Participant.identifier == identifier)
            result = await session.execute(stmt)
            participant = result.scalars().first()
            if participant:
                # Construct and return a ParticipantType
                return ParticipantType(
                    id=participant.id,
                    identifier=participant.identifier,
                    metadata=participant.meta_data,
                    createdAt=participant.createdAt,
                )
            # Return None if no participant is found
            return None

    @staticmethod
    async def get_by_id_or_identifier(
        id: Optional[str] = None, identifier: Optional[str] = None
    ) -> Optional[Participant]:
        async for session in db.get_db():
            # Construct the base query
            query = select(Participant)

            # Add conditions based on provided parameters
            conditions = []
            if id:
                conditions.append(Participant.id == id)
            if identifier:
                conditions.append(Participant.identifier == identifier)

            # If no valid conditions are provided, return None
            if not conditions:
                return None

            # Apply conditions to the query
            query = query.where(or_(*conditions))

            # Execute the query
            result = await session.execute(query)
            return result.scalars().first()


participant_repo = ParticipantRepository()
