import strawberry
from typing import Optional
from enum import Enum


@strawberry.enum
class FeedbackStrategy(Enum):
    BINARY = "BINARY"
    STARS = "STARS"
    BIG_STARS = "BIG_STARS"
    LIKERT = "LIKERT"
    CONTINUOUS = "CONTINUOUS"
    LETTERS = "LETTERS"
    PERCENTAGE = "PERCENTAGE"


@strawberry.type
class FeedbackType:
    id: Optional[str]
    threadId: Optional[str]
    value: Optional[float]
    strategy: Optional[FeedbackStrategy]
    comment: Optional[str]
    stepId: Optional[str]


@strawberry.input
class FeedbackPayloadInput:
    comment: Optional[str]
    strategy: Optional[FeedbackStrategy]
    value: Optional[int]
