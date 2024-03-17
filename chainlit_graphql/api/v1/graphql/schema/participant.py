import strawberry
from typing import Optional
from datetime import datetime
from ..scalars.json_scalar import Json


@strawberry.type
class ParticipantType:
    id: Optional[str]
    identifier: Optional[str]
    metadata: Optional[Json]
    createdAt: datetime


@strawberry.input
class ParticipantInput:
    id: Optional[str] = None
    identifier: Optional[str] = None
    metadata: Optional[Json] = None
