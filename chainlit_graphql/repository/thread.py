from chainlit_graphql.model.participant import Participant
from chainlit_graphql.model.thread import Thread
from chainlit_graphql.model.step import Step
import strawberry
from chainlit_graphql.api.v1.graphql.scalars.json_scalar import Json
from chainlit_graphql.api.v1.graphql.schema.thread import (
    ThreadType,
    ThreadConnection,
    ThreadEdge,
    PageInfo,
    ParticipantType,
    ThreadsInputType,
)
from chainlit_graphql.db.database import db
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import desc, update, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime, timezone
import base64

from chainlit_graphql.core.mappers import MapperUtility


class ThreadRepository:

    async def get_paginated_threads(
        self,
        after: Optional[strawberry.ID] = None,
        before: Optional[strawberry.ID] = None,
        cursorAnchor: Optional[datetime] = None,
        filters: Optional[List[ThreadsInputType]] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        projectId: Optional[str] = None,
        skip: Optional[int] = None,
    ) -> ThreadConnection:
        async for session in db.get_db():
            try:
                # Base query
                query = (
                    select(Thread)
                    .options(
                        selectinload(Thread.steps).selectinload(Step.scores),
                        selectinload(Thread.participant),
                    )
                    .order_by(desc(Thread.createdAt))
                )

                # Apply cursor anchor conditions
                if cursorAnchor:
                    if after:
                        query = query.where(Thread.createdAt > cursorAnchor)
                    elif before:
                        query = query.where(Thread.createdAt < cursorAnchor)

                # Apply cursor-based pagination
                if after:
                    cursor_id = base64.b64decode(after).decode().split(":")[1]
                    query = query.where(Thread.id > cursor_id)
                if before:
                    cursor_id = base64.b64decode(before).decode().split(":")[1]
                    query = query.where(Thread.id < cursor_id)

                # Apply additional filters (if provided)
                if filters:
                    for filter in filters:
                        if filter.field == "participantId":
                            # Extract the operator and values from the filter
                            operator = filter.operator
                            identifiers = filter.value

                            # Apply filter based on the operator
                            if operator == "eq":
                                query = query.where(Thread.participantId == identifiers)
                            elif operator == "in":
                                participant_ids = await session.execute(
                                    select(Participant.id).where(
                                        Participant.identifier.in_(identifiers)
                                    )
                                )
                                participant_ids_list = [id[0] for id in participant_ids]
                                query = query.join(Thread.participant).where(
                                    Participant.id.in_(participant_ids_list)
                                )
                            elif operator == "nin":
                                participant_ids = await session.execute(
                                    select(Participant.id).where(
                                        Participant.identifier.in_(identifiers)
                                    )
                                )
                                participant_ids_list = [id[0] for id in participant_ids]
                                query = query.join(Thread.participant).where(
                                    ~Participant.id.in_(participant_ids_list)
                                )

                # Skip and limit
                if skip is not None:
                    query = query.offset(skip)
                if first is not None:
                    query = query.limit(first)
                elif last is not None:
                    query = query.limit(last)

                # Execute query for threads
                result = await session.execute(query)
                threads = result.scalars().all()
                # Manually fetch steps and participant for each thread
                edges = []
                for thread in threads:
                    thread_type = await ThreadRepository.map_to_thread_type(thread)
                    edges.append(
                        ThreadEdge(
                            node=thread_type,
                            cursor=base64.b64encode(
                                f"Thread:{thread.id}".encode()
                            ).decode(),
                        )
                    )

                # Check for more pages
                has_next_page = False
                has_previous_page = False

                if len(threads) > 0 and first is not None:
                    next_page_check_query = select(Thread).where(
                        Thread.id > threads[-1].id
                    )
                    next_page_check_result = await session.execute(
                        next_page_check_query
                    )
                    has_next_page = next_page_check_result.scalar() is not None

                if len(threads) > 0 and (after is not None or before is not None):
                    prev_page_check_query = select(Thread).where(
                        Thread.id < threads[0].id
                    )
                    prev_page_check_result = await session.execute(
                        prev_page_check_query
                    )
                    has_previous_page = prev_page_check_result.scalar() is not None

                # PageInfo using first and last thread IDs for cursors
                start_cursor = edges[0].cursor if edges else None
                end_cursor = edges[-1].cursor if edges else None

                page_info = PageInfo(
                    has_next_page=has_next_page,
                    has_previous_page=has_previous_page,
                    start_cursor=start_cursor,
                    end_cursor=end_cursor,
                )

                return ThreadConnection(
                    edges=edges, page_info=page_info, total_count=len(edges)
                )
            except Exception as e:
                print("Failed to get paginated threads: %s", e)
                raise e

    async def upsert_thread(
        self,
        id: Optional[str],
        name: Optional[str],
        tags: Optional[List[str]],
        metadata: Optional[Json],
        participantId: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> ThreadType:
        async with db.SessionLocal() as session:
            async with session.begin():  # Start a transaction
                try:
                    if id:
                        try:
                            # Attempt to decode as base64
                            decoded_id = base64.b64decode(id).decode()
                            # Extract the ID part if it follows the 'Type:id' format
                            if ":" in decoded_id:
                                id = decoded_id.split(":")[1]
                        except (base64.binascii.Error, UnicodeDecodeError):
                            # If decoding fails, assume it's a regular UUID and do nothing
                            pass
                        existing_thread = await thread_repo.get_by_id(id, session)
                        if existing_thread:
                            if name is not None:
                                existing_thread.name = name
                            if metadata is not None:
                                # Ensure existing metadata is a dictionary
                                if existing_thread.meta_data is None:
                                    existing_thread.meta_data = {}

                                # Update existing meta_data with new meta_data
                                for key, value in metadata.items():
                                    existing_thread.meta_data[key] = value
                            if environment is not None:
                                existing_thread.environment = environment
                            if tags is not None:
                                existing_thread.tags = tags

                            updated_thread = await ThreadRepository.update(
                                id, existing_thread, session
                            )

                            # await session.commit()

                            thread_type = await ThreadRepository.map_to_thread_type(
                                updated_thread
                            )

                            if not updated_thread:
                                raise ValueError(f"Thread with id {id} not found")

                            return thread_type

                        else:
                            # Check for inferred deletion context
                            if participantId is None:
                                # Skip insertion since it might be a deletion context
                                return None
                            thread_to_create = Thread(
                                id=id,
                                name=name,
                                meta_data=metadata,
                                participant_id=participantId,
                                environment=environment,
                                tags=tags,
                                createdAt=datetime.now(timezone.utc),
                            )
                            created_thread = await ThreadRepository.create(
                                thread_to_create, session
                            )

                            thread_type = await ThreadRepository.map_to_thread_type(
                                created_thread
                            )

                            # await session.commit()
                            return thread_type

                    return None

                except Exception as e:
                    await session.rollback()
                    raise e

    async def _get_by_id_with_session(self, id: str) -> Optional[Thread]:
        async for session in db.get_db():
            try:  # Attempt to decode as base64
                decoded_id = base64.b64decode(id).decode()
                # Extract the ID part if it follows the 'Type:id' format
                if ":" in decoded_id:
                    id = decoded_id.split(":")[1]
            except (base64.binascii.Error, UnicodeDecodeError):
                # If decoding fails, assume it's a regular UUID and do nothing
                pass
            stmt = (
                select(Thread)
                .where(Thread.id == id)
                .options(
                    joinedload(Thread.steps).joinedload(Step.scores),
                    joinedload(Thread.participant),
                )
                .order_by(text('"steps_1"."createdAt"'))
            )

            result = await session.execute(stmt)
            model = result.scalars().first()

            if model:
                # If using its own session, call the additional method
                return await ThreadRepository.map_to_thread_type(model)

            return None

    async def get_by_id(self, id: str, session) -> Optional[Thread]:
        try:
            stmt = (
                select(Thread)
                .where(Thread.id == id)
                .options(
                    joinedload(Thread.steps).joinedload(Step.scores),
                    joinedload(Thread.participant),
                )
                .order_by(text('"steps_1"."createdAt"'))
            )

            result = await session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            print(f"An error occurred while retrieving the thread: {e}")
            await session.rollback()
            raise e

    @staticmethod
    async def update(id: Optional[str], model: Thread, session) -> Optional[Thread]:
        if id:
            # Construct the update statement
            stmt = (
                update(Thread)
                .where(Thread.id == id)
                .values(
                    name=model.name,
                    meta_data=model.meta_data,
                    environment=model.environment,
                    tags=model.tags,
                )
            )

            # Execute the update statement
            await session.execute(stmt)
            await session.flush()

            # Retrieve the updated model with eager loading for steps and their score, and participant
            result = await session.execute(
                select(Thread)
                .where(Thread.id == id)
                .options(
                    selectinload(Thread.steps).selectinload(Step.scores),
                    selectinload(Thread.participant),
                )
            )
            updated_model = result.scalars().first()

            return updated_model
        else:
            return None

    @staticmethod
    async def create(thread_data: Thread, session) -> Thread:
        # Add the new Thread to the session
        session.add(thread_data)
        await session.flush()

        # Retrieve the created Thread with eager loading for steps and their scores, and participant
        result = await session.execute(
            select(Thread)
            .where(Thread.id == thread_data.id)
            .options(
                selectinload(Thread.steps).selectinload(Step.scores),
                selectinload(Thread.participant),
            )
        )
        created_thread = result.scalars().first()

        return created_thread

    @staticmethod
    async def map_to_thread_type(thread_model) -> ThreadType:
        try:
            steps_types = [
                await MapperUtility.map_step_to_stepstype(step)
                for step in thread_model.steps
            ]

            participant = None
            if thread_model.participant:
                participant = ParticipantType(
                    id=thread_model.participant.id,
                    identifier=thread_model.participant.identifier,
                    metadata=thread_model.participant.meta_data,
                    createdAt=thread_model.participant.createdAt,
                )

            # Return ThreadType with all mapped information
            return ThreadType(
                id=thread_model.id,
                name=thread_model.name,
                metadata=thread_model.meta_data,
                environment=thread_model.environment,
                tags=thread_model.tags,
                createdAt=thread_model.createdAt,
                participant_id=thread_model.participant_id,
                steps=steps_types,
                participant=participant,
            )

        except SQLAlchemyError as e:
            # Handle specific SQLAlchemy errors
            print(f"SQLAlchemyError during map_to_thread_type: {e}")
            raise e
        except Exception as e:
            # Handle general exceptions
            print(f"General error during map_to_thread_type: {e}")
            raise e

    async def delete(self, thread_id: str) -> ThreadType:
        async for session in db.get_db():
            try:
                # Attempt to decode as base64
                try:
                    decoded_id = base64.b64decode(thread_id).decode()
                    # Extract the ID part if it follows the 'Type:id' format
                    if ":" in decoded_id:
                        thread_id = decoded_id.split(":")[1]
                except (base64.binascii.Error, UnicodeDecodeError):
                    # If decoding fails, assume it's a regular UUID and do nothing
                    pass

                # Fetch the thread to be deleted
                thread_to_delete = await thread_repo.get_by_id(thread_id, session)

                # If the thread exists, delete it
                if thread_to_delete:
                    await session.delete(thread_to_delete)
                    await session.commit()

                    # Return a basic ThreadType object with just the id
                    return ThreadType(id=thread_id)
                else:
                    # Handle the case where the thread does not exist
                    # Here, you might want to return None or raise an exception
                    return None

            except Exception as e:
                await session.rollback()
                print(f"An error occurred during deletion: {e}")
                raise e


thread_repo = ThreadRepository()
