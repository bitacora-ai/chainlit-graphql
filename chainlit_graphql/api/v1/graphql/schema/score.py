import strawberry
from typing import List, Optional
from enum import Enum


@strawberry.enum
class ScoreType(Enum):
    AI = "AI"
    HUMAN = "HUMAN"


@strawberry.type
class Score:
    id: Optional[str]
    name: Optional[str]
    type: Optional[ScoreType]
    value: Optional[float]
    stepId: Optional[str]
    generationId: Optional[str]
    datasetExperimentItemId: Optional[str]
    comment: Optional[str]
    tags: Optional[List[str]]
