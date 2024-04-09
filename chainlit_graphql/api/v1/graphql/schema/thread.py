import strawberry
from strawberry import relay
from .step import StepsType
from .participant import ParticipantType
from ..scalars.json_scalar import Json, Unknown
from typing import Optional, List
from datetime import datetime
from enum import Enum


@strawberry.type
class ThreadType(relay.Node):
    id: relay.NodeID[str]
    name: Optional[str] = None
    metadata: Optional[Json] = None
    tokenCount: Optional[int] = None
    environment: Optional[str] = None
    tags: Optional[List[str]] = None
    createdAt: datetime = None
    participant_id: Optional[str] = None
    steps: Optional[List[StepsType]] = None
    participant: Optional[ParticipantType] = None
    duration: Optional[int] = None


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
class FilterOperatorEnum(Enum):
    alternate_neq = "alternate_neq"
    double_eq = "double_eq"
    eq = "eq"
    exists = "exists"
    exists_key = "exists_key"
    gt = "gt"
    gte = "gte"
    ilike = "ilike"
    ilike_regexp = "ilike_regexp"
    # in_ = "in"  # Adjusted for Python
    # is_ = "is"
    like = "like"
    lt = "lt"
    lte = "lte"
    match = "match"
    neq = "neq"
    ngt = "ngt"
    nilike = "nilike"
    nilike_regexp = "nilike_regexp"
    nin = "nin"
    nis = "nis"
    nlike = "nlike"
    nlt = "nlt"
    nregexp = "nregexp"
    null_safe_eq = "null_safe_eq"
    overlap = "overlap"
    regexp = "regexp"
    regexp_match = "regexp_match"
    text_search = "text_search"
    text_search_or = "text_search_or"


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


@strawberry.enum
class FilterAccessorEnum(Enum):
    json_get = "json_get"
    text_get = "text_get"


@strawberry.enum
class ThreadsFieldEnumType(Enum):
    createdAt = "createdAt"
    duration = "duration"
    environment = "environment"
    id = "id"
    metadata = "metadata"
    name = "name"
    participantId = "participantId"
    participantIdentifiers = "participantIdentifiers"
    scoreValue = "scoreValue"
    stepName = "stepName"
    stepOutput = "stepOutput"
    stepType = "stepType"
    tags = "tags"
    tokenCount = "tokenCount"


@strawberry.input
class StringOrFloat:
    stringValue: Optional[str] = None
    floatValue: Optional[float] = None


@strawberry.input
class ThreadsInputType:
    accessor: Optional[FilterAccessorEnum] = None
    field: ThreadsFieldEnumType
    operator: FilterOperatorEnum
    path: List[StringOrFloat] = None
    value: Optional[Unknown] = strawberry.auto


@strawberry.enum
class ThreadsOrderByInputColumn(Enum):
    createdAt = "createdAt"
    participant = "participant"
    tokenCount = "tokenCount"


@strawberry.enum
class Direction(Enum):
    ASC = "ASC"
    DESC = "DESC"


@strawberry.input
class ThreadsOrderByInput:
    column: Optional[ThreadsOrderByInputColumn] = None
    direction: Optional[Direction] = None
