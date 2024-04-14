from chainlit_graphql.api.v1.graphql.schema.score import Score, ScoreType
from chainlit_graphql.service.score import ScoreService
import strawberry
from typing import Optional, List

from chainlit_graphql.api.deps import IsValidApiKey
from chainlit_graphql.service.participant import ParticipantService
from chainlit_graphql.service.step import StepService
from chainlit_graphql.service.thread import ThreadService
from chainlit_graphql.repository.participant import participant_repo
from chainlit_graphql.repository.thread import thread_repo
from chainlit_graphql.repository.score import score_repo
from chainlit_graphql.repository.step import step_repo
from ..schema.step import (
    AttachmentPayloadInput,
    ScorePayloadInput,
    StepsType,
    StepType,
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
        tags: Optional[List[str]] = None,
        scores: Optional[List[ScorePayloadInput]] = None,
        generation: Optional[GenerationPayloadInput] = None,
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
            tags,  
            scores,
            generation,
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
    async def createScore(
        self,
        name: str,
        type: ScoreType,
        value: float,
        stepId: Optional[str] = None,
        generationId: Optional[str] = None,
        datasetExperimentItemId: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Score:
        score_service = ScoreService(score_repository=score_repo)
        return await score_service.add_score(
            name=name,
            type=type,
            value=value,
            stepId=stepId,
            generationId=generationId,
            datasetExperimentItemId=datasetExperimentItemId,
            comment=comment,
            tags=tags,
        )

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def updateScore(
        self,
        id: str,
        name: Optional[str] = None,
        type: Optional[ScoreType] = None,
        value: Optional[float] = None,
        stepId: Optional[str] = None,
        generationId: Optional[str] = None,
        datasetExperimentItemId: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Score:
        score_service = ScoreService(score_repository=score_repo)
        updated_score = await score_service.update_score(
            id=id,
            name=name,
            type=type,
            value=value,
            stepId=stepId,
            generationId=generationId,
            datasetExperimentItemId=datasetExperimentItemId,
            comment=comment,
            tags=tags,
        )
        if updated_score:
            return updated_score
        else:
            raise ValueError(f"Score with id {id} not found")

    @strawberry.mutation(permission_classes=[IsValidApiKey])
    async def deleteScore(self, id: str) -> Optional[Score]:
        score_service = ScoreService(score_repository=score_repo)
        deleted_score = await score_service.delete(id)
        return deleted_score
