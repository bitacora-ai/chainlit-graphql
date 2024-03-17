from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict
from datetime import datetime, timezone
from sqlalchemy import Column, JSON
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .thread import Thread
    from .feedback import Feedback


class Step(SQLModel, table=True):
    __tablename__ = "steps"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    thread_id: Optional[str] = Field(default=None, foreign_key="threads.id")
    parent_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: Optional[str] = None
    error: Optional[str] = None
    input: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    output: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    meta_data: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    name: Optional[str] = None
    generation: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    attachments: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    createdAt: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )
    thread: "Thread" = Relationship(back_populates="steps")
    feedback: Optional["Feedback"] = Relationship(
        back_populates="step",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "uselist": False},
    )
    thread: "Thread" = Relationship(back_populates="steps")

    class Config:
        arbitrary_types_allowed = True
