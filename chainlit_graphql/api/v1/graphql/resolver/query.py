import strawberry

from chainlit_graphql.service.participant import ParticipantService
from chainlit_graphql.service.thread import ThreadService
from chainlit_graphql.repository.participant import participant_repo
from chainlit_graphql.repository.thread import thread_repo
from typing import List, Optional
from ..schema.participant import ParticipantType
from ..schema.thread import (
    ThreadsInputType,
    ThreadType,
    ThreadConnection,
    ThreadsOrderByInput,
)
from chainlit_graphql.api.deps import IsValidApiKey
from datetime import datetime


@strawberry.type
class Query:

    @strawberry.field(permission_classes=[IsValidApiKey])
    def hello(self) -> str:
        return "Hello World!"

    @strawberry.field(permission_classes=[IsValidApiKey])
    async def get_by_id(self, id: str, identifier: str) -> ParticipantType:
        participant_service = ParticipantService(participant_repo)
        return await participant_service.get_by_id(id, identifier)

    @strawberry.field(permission_classes=[IsValidApiKey])
    async def threadDetail(self, id: str) -> ThreadType:
        thread_service = ThreadService(thread_repo)
        return await thread_service.get_by_id(id)

    @strawberry.field(permission_classes=[IsValidApiKey])
    async def participant(
        self, id: Optional[str] = None, identifier: Optional[str] = None
    ) -> Optional[ParticipantType]:
        participant_service = ParticipantService(participant_repo)
        return await participant_service.get_by_id_or_identifier(id, identifier)

    @strawberry.field(permission_classes=[IsValidApiKey])
    async def threads(
        self,
        after: Optional[strawberry.ID] = None,
        before: Optional[strawberry.ID] = None,
        cursorAnchor: Optional[datetime] = None,
        filters: Optional[List[ThreadsInputType]] = None,
        orderBy: Optional[ThreadsOrderByInput] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        projectId: Optional[str] = None,
        skip: Optional[int] = None,
    ) -> ThreadConnection:
        # if filters.operator not in [
        #     operator.value for operator in FilterOperator
        # ]:
        #     raise ValueError("Invalid operator")
        thread_service = ThreadService(thread_repo)
        return await thread_service.get_threads_paginated(
            after=after,
            before=before,
            cursorAnchor=cursorAnchor,
            filters=filters,
            first=first,
            last=last,
            projectId=projectId,
            skip=skip,
        )
