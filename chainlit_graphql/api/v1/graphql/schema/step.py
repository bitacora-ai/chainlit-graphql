import strawberry
from typing import Optional, List
from .feedback import FeedbackType
from datetime import datetime
from enum import Enum
from ..scalars.json_scalar import Json


@strawberry.input
class GenerationPayloadInput:
    type: Optional[str] = None
    prompt: Optional[str] = None
    provider: Optional[str] = None
    settings: Optional[Json] = None
    stepId: Optional[str] = None
    variables: Optional[Json] = None
    inputs: Optional[Json] = None
    duration: Optional[str] = None
    model: Optional[str] = None
    ttFirstToken: Optional[str] = None
    completion: Optional[str] = None
    createdAt: Optional[datetime] = None
    tokenThroughputInSeconds: Optional[str] = None
    tags: Optional[List[str]] = None
    error: Optional[str] = None
    tools: Optional[List[str]] = None
    inputTokenCount: Optional[str] = None
    outputTokenCount: Optional[str] = None
    messageCompletion: Optional[str] = None
    templateFormat: Optional[str] = None
    template: Optional[str] = None
    formatted: Optional[str] = None
    messages: Optional[Json] = None
    tokenCount: Optional[int] = None


@strawberry.type
class GenerationType:
    type: Optional[str] = None
    prompt: Optional[str] = None
    provider: Optional[str] = None
    settings: Optional[Json] = None
    stepId: Optional[str] = None
    variables: Optional[Json] = None
    inputs: Optional[Json] = None
    duration: Optional[str] = None
    model: Optional[str] = None
    ttFirstToken: Optional[str] = None
    completion: Optional[str] = None
    createdAt: Optional[datetime] = None
    tokenThroughputInSeconds: Optional[str] = None
    tags: Optional[List[str]] = None
    error: Optional[str] = None
    tools: Optional[List[str]] = None
    inputTokenCount: Optional[str] = None
    outputTokenCount: Optional[str] = None
    messageCompletion: Optional[str] = None
    templateFormat: Optional[str] = None
    template: Optional[str] = None
    formatted: Optional[str] = None
    messages: Optional[Json] = None
    tokenCount: Optional[int] = None


@strawberry.type
class AttachmentType:
    id: Optional[str] = None
    threadId: Optional[str] = None
    stepId: Optional[str] = None
    metadata: Optional[Json] = None
    mime: Optional[str] = None
    name: Optional[str] = None
    objectKey: Optional[str] = None
    url: Optional[str] = None


@strawberry.input
class AttachmentPayloadInput:
    id: Optional[str] = None
    metadata: Optional[Json] = None
    mime: Optional[str] = None
    name: Optional[str] = None
    objectKey: Optional[str] = None
    url: Optional[str] = None


@strawberry.enum
class StepType(Enum):
    run = "run"
    tool = "tool"
    llm = "llm"
    embedding = "embedding"
    retrieval = "retrieval"
    rerank = "rerank"
    undefined = "undefined"
    user_message = "user_message"
    assistant_message = "assistant_message"
    system_message = "system_message"


@strawberry.type
class StepsType:
    id: str
    thread_id: Optional[str] = None
    parent_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    createdAt: datetime
    type: Optional[StepType] = None
    error: Optional[str] = None
    input: Optional[Json] = None
    tags: Optional[List[str]] = None
    output: Optional[Json] = None
    metadata: Optional[Json] = None
    name: Optional[str] = None
    feedback: Optional[FeedbackType] = None
    generation: Optional[GenerationType] = None
    attachments: Optional[List[AttachmentType]] = None
    ok: Optional[bool] = True
    message: Optional[str] = "Step added success"
