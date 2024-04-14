from chainlit_graphql.model.step import Step
from chainlit_graphql.repository.thread import thread_repo
from chainlit_graphql.api.v1.graphql.schema.step import (
    AttachmentPayloadInput,
    ScorePayloadInput,
    StepsType,
    GenerationPayloadInput,
)
from chainlit_graphql.db.database import db
from datetime import datetime, timezone
import asyncio
from typing import Optional, List
from ..core.mappers import MapperUtility
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert
from ..api.v1.graphql.scalars.json_scalar import Json


class StepRepository:

    async def upsert_step(
        self,
        id: str,
        threadId: str,
        startTime: Optional[datetime] = None,
        endTime: Optional[datetime] = None,
        type: Optional[str] = None,
        error: Optional[str] = None,
        input: Optional[Json] = None,
        output: Optional[Json] = None,
        metadata: Optional[Json] = None,
        parentId: Optional[str] = None,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None, 
        scores: Optional[List[ScorePayloadInput]] = None,
        generation: Optional[GenerationPayloadInput] = None,
        attachments: Optional[List[AttachmentPayloadInput]] = None,
    ) -> StepsType:
        async with db.SessionLocal() as session:
            async with session.begin():  # Start a transaction
                try:
                    # Polling to check if the parent thread exists and is ready
                    max_attempts = 10
                    attempt = 0
                    parent_thread_ready = False
                    while attempt < max_attempts and not parent_thread_ready:
                        parent_thread = await thread_repo.get_by_id(threadId, session)
                        if parent_thread is not None:
                            parent_thread_ready = True
                        else:
                            await asyncio.sleep(0.2)
                            attempt += 1

                    if not parent_thread_ready:
                        raise Exception("Parent thread not ready within expected time.")

                    insert_values = {
                        key: value
                        for key, value in {
                            "id": id,
                            "thread_id": threadId,
                            "start_time": startTime,
                            "end_time": endTime,
                            "type": type,
                            "error": error,
                            "input": input,
                            "output": output,
                            "meta_data": metadata,
                            "parent_id": parentId,
                            "name": name,
                            "tags": tags, 
                            "scores": scores,
                            "generation": (
                                MapperUtility.serialize_generation_payload(generation)
                                if generation is not None
                                else None
                            ),
                            "attachments": (
                                MapperUtility.serialize_attachments_payload(attachments)
                                if attachments is not None
                                else None
                            ),
                            "createdAt": datetime.now(timezone.utc),
                        }.items()
                        if value is not None
                    }

                    # Execute an upsert using SQLAlchemy's Core expression language
                    stmt = (
                        insert(Step)
                        .values(**insert_values)
                        .on_conflict_do_update(
                            index_elements=[
                                "id"
                            ],  # Specify the constraint (primary key) causing the conflict
                            set_={
                                k: v
                                for k, v in insert_values.items()
                                if v is not None and k != "id"
                            },
                        )
                    )
                    await session.execute(stmt)

                    # Retrieve the updated/inserted step
                    updated_step = await session.get(
                        Step, id, options=[joinedload(Step.scores)]
                    )

                    # Map the updated_step to the schema
                    step_type = await MapperUtility.map_step_to_stepstype(updated_step)

                    return step_type

                except Exception as e:
                    await session.rollback()
                    raise e


step_repo = StepRepository()
