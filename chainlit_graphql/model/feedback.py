from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .step import Step


class Feedback(SQLModel, table=True):
    __tablename__ = "feedback"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    value: Optional[float]
    strategy: Optional[str] = "BINARY"
    comment: Optional[str]
    step_id: Optional[str] = None
    thread_id: Optional[str] = None
    step_id: Optional[str] = Field(default=None, foreign_key="steps.id")
    step: Optional["Step"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "single_parent": True}
    )
