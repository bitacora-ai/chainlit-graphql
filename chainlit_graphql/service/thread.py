from chainlit_graphql.repository.thread import ThreadRepository
from chainlit_graphql.api.v1.graphql.schema.thread import ThreadType, ThreadConnection
from chainlit_graphql.api.v1.graphql.schema.thread import ThreadsInputType
from typing import Optional, List
from datetime import datetime
import strawberry
from chainlit_graphql.api.v1.graphql.scalars.json_scalar import Json
import json


class ThreadService:
    def __init__(self, thread_repository: ThreadRepository):
        self.thread_repository = thread_repository

    async def add_thread(
        self,
        name: Optional[str],
        metadata: Optional[Json],
        participantId: Optional[str],
        environment: Optional[str],
        tags: List[str],
    ) -> ThreadType:

        tags_json = json.dumps(tags) if tags else None
        metadata = json.loads(metadata)

        # Create and save the new Thread
        thread = await self.thread_repository.upsert_thread(
            name, metadata, participantId, environment, tags_json
        )

        return thread

    async def get_threads_paginated(
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
        # Call the get_paginated_threads method with all the parameters
        return await self.thread_repository.get_paginated_threads(
            after=after,
            before=before,
            cursorAnchor=cursorAnchor,
            filters=filters,
            first=first,
            last=last,
            projectId=projectId,
            skip=skip,
        )

    async def get_by_id(self, id: str):
        thread = await self.thread_repository._get_by_id_with_session(id)
        return thread

    async def upsert_thread(
        self,
        id: Optional[str],
        name: Optional[str],
        tags: Optional[List[str]],
        metadata: Optional[Json],
        participantId: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> Optional[ThreadType]:

        # Parse metadata and tags
        # metadata_obj = json.loads(metadata) if metadata else None
        tags_json = tags if tags is not None else []

        thread = await self.thread_repository.upsert_thread(
            id,
            name,
            tags_json,
            metadata,
            participantId,
            environment,
        )

        return thread

    async def delete(self, id: str) -> ThreadType:
        thread = await self.thread_repository.delete(id)
        return thread
