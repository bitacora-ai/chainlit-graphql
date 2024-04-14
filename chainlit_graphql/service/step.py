from chainlit_graphql.repository.step import StepRepository
from chainlit_graphql.api.v1.graphql.schema.step import (
    ScorePayloadInput,
    StepsType,
    StepType,
    GenerationPayloadInput,
    AttachmentPayloadInput,
)
from typing import Optional, List
from datetime import datetime
from chainlit_graphql.api.v1.graphql.scalars.json_scalar import Json
import base64


class StepService:
    def __init__(self, step_repository: StepRepository):
        self.step_repository = step_repository

    async def upsert(
        self,
        id: str,
        threadId: str,
        startTime: Optional[datetime] = None,
        endTime: Optional[datetime] = None,
        type: Optional[StepType] = None,
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
    ) -> Optional[StepsType]:

        try:
            # Attempt to decode as base64
            decoded_id = base64.b64decode(threadId).decode()
            # Extract the ID part if it follows the 'Type:id' format
            if ":" in decoded_id:
                threadId = decoded_id.split(":")[1]
        except (base64.binascii.Error, UnicodeDecodeError):
            # If decoding fails, assume it's a regular UUID and do nothing
            pass

        type_str = type.value if type else None

        created_step = await self.step_repository.upsert_step(
            id,
            threadId,
            startTime,
            endTime,
            type_str,
            error,
            input,
            output,
            metadata,
            parentId,
            name,
            tags,
            scores,
            generation,
            attachments,
        )

        return created_step
