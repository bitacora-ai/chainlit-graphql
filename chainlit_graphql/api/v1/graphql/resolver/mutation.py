import strawberry
from typing import Optional, List

from chainlit_graphql.api.deps import IsValidApiKey
from chainlit_graphql.service.participant import ParticipantService
from chainlit_graphql.service.step import StepService
from chainlit_graphql.service.thread import ThreadService
from chainlit_graphql.service.feedback import FeedbackService
from chainlit_graphql.repository.participant import participant_repo
from chainlit_graphql.repository.thread import thread_repo
from chainlit_graphql.repository.feedback import feedback_repo
from chainlit_graphql.repository.step import step_repo
from ..schema.feedback import FeedbackPayloadInput, FeedbackStrategy
from ..schema.step import (
    AttachmentPayloadInput,
    StepsType,
    StepType,
    FeedbackType,
    GenerationPayloadInput,
)
from ..schema.thread import ThreadType
from ..schema.participant import ParticipantType
from ..scalars.json_scalar import Json
from datetime import datetime


@strawberry.type
class Mutation:

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def createParticipant(
        self, identifier: str, metadata: Optional[Json] = None
    ) -> Optional[ParticipantType]:
        participant_service = ParticipantService(participant_repo)
        return await participant_service.add_participant(identifier, metadata)

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def updateParticipant(
        self, id: str, identifier: Optional[str] = None, metadata: Optional[Json] = None
    ) -> Optional[ParticipantType]:
        participant_service = ParticipantService(participant_repo)
        return await participant_service.update(id, identifier, metadata)

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def deleteParticipant(self, id: str) -> str:
        participant_service = ParticipantService(participant_repo)
        return await participant_service.delete(id)

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def deleteThread(self, id: str) -> Optional[ThreadType]:
        thread_service = ThreadService(thread_repo)
        thread = await thread_service.delete(id)
        return thread

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def updateFeedback(
        self,
        id: str,
        comment: Optional[str],
        value: Optional[int],
        strategy: Optional[FeedbackStrategy],
    ) -> Optional[FeedbackType]:
        feedback_service = FeedbackService(feedback_repo)
        return await feedback_service.update(id, comment, value, strategy)

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def upsertThread(
        self,
        id: str,
        name: Optional[str] = None,
        metadata: Optional[Json] = None,
        participantId: Optional[str] = None,
        environment: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[ThreadType]:
        thread_service = ThreadService(thread_repo)
        return await thread_service.upsert_thread(
            id=id,
            name=name,
            metadata=metadata,
            participantId=participantId,
            environment=environment,
            tags=tags,
        )

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def ingestStep(
        self,
        id: str,
        threadId: Optional[str] = None,
        startTime: Optional[datetime] = None,
        endTime: Optional[datetime] = None,
        type: Optional[StepType] = None,
        error: Optional[str] = None,
        input: Optional[Json] = None,
        output: Optional[Json] = None,
        metadata: Optional[Json] = None,
        parentId: Optional[str] = None,
        name: Optional[str] = None,
        generation: Optional[GenerationPayloadInput] = None,
        feedback: Optional[FeedbackPayloadInput] = None,
        attachments: Optional[List[AttachmentPayloadInput]] = None,
    ) -> Optional[StepsType]:
        step_service = StepService(step_repo)
        return await step_service.upsert(
            id,
            threadId,
            startTime,
            endTime,
            type,
            error,
            input,
            output,
            metadata,
            parentId,
            name,
            generation,
            feedback,
            attachments,
        )

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def createThread(
        self,
        name: Optional[str],
        metadata: Optional[Json],
        participantId: Optional[str],
        environment: Optional[str],
        tags: List[str],
    ) -> Optional[ThreadType]:
        thread_service = ThreadService(thread_repo)
        return await thread_service.add_thread(
            name, metadata, participantId, environment, tags
        )

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def createFeedback(
        self,
        comment: Optional[str],
        stepId: str,
        strategy: Optional[FeedbackStrategy],
        value: int,
    ) -> Optional[FeedbackType]:
        feedback_service = FeedbackService(feedback_repo)
        return await feedback_service.add_feedback(comment, stepId, strategy, value)
