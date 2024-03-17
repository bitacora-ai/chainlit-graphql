import strawberry
from strawberry import relay
from .step import StepsType
from .participant import ParticipantType
from ..scalars.json_scalar import Json
from typing import Optional, List
from datetime import datetime
from enum import Enum


@strawberry.type
class ThreadType(relay.Node):
    id: relay.NodeID[str]
    name: Optional[str] = None
    metadata: Optional[Json] = None
    environment: Optional[str] = None
    tags: Optional[List[str]] = None
    createdAt: datetime = None
    participant_id: Optional[str] = None
    steps: Optional[List[StepsType]] = None
    participant: Optional[ParticipantType] = None


@strawberry.type
class ThreadEdge(relay.Edge):
    node: Optional[ThreadType] = None


@strawberry.type
class PageInfo:
    has_next_page: Optional[bool] = None
    has_previous_page: Optional[bool] = None
    start_cursor: Optional[str] = None
    end_cursor: Optional[str] = None


@strawberry.type
class ThreadConnection(relay.Connection):
    edges: Optional[List[ThreadEdge]] = None
    page_info: Optional[PageInfo] = None
    total_count: Optional[int] = None


@strawberry.enum
class StringOperators(Enum):
    eq = "eq"
    ilike = "ilike"
    like = "like"
    neq = "neq"
    nilike = "nilike"
    nlike = "nlike"


@strawberry.enum
class StringListOperators(Enum):
    in_ = "in"
    nin = "nin"


@strawberry.enum
class NumberListOperators(Enum):
    in_ = "in"
    nin = "nin"


@strawberry.enum
class NumberOperators(Enum):
    eq = "eq"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"
    neq = "neq"


@strawberry.enum
class DateTimeOperators(Enum):
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"


@strawberry.input
class StringListFilter:
    operator: str
    value: List[str]


@strawberry.input
class DateTimeFilter:
    operator: DateTimeOperators
    value: str


@strawberry.input
class NumberFilter:
    operator: NumberOperators
    value: float


@strawberry.input
class StringFilter:
    operator: StringOperators
    value: str


@strawberry.input
class NumberListFilter:
    operator: str
    value: List[float]


@strawberry.input
class ThreadFiltersInput:
    attachmentsName: Optional[StringListFilter] = None
    createdAt: Optional[DateTimeFilter] = None
    afterCreatedAt: Optional[DateTimeFilter] = None
    beforeCreatedAt: Optional[DateTimeFilter] = None
    duration: Optional[NumberFilter] = None
    environment: Optional[StringFilter] = None
    feedbacksValue: Optional[NumberListFilter] = None
    participantsIdentifier: Optional[StringListFilter] = None
    search: Optional[StringFilter] = None
    tokenCount: Optional[NumberFilter] = None
