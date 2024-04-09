from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, JSON
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .thread import Thread
    from .score import Score


class Step(SQLModel, table=True):
    __tablename__ = "steps"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    thread_id: Optional[str] = Field(default=None, foreign_key="threads.id")
    parent_id: Optional[str] = None
    start_time: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True)))
    end_time: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True)))
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
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    thread: "Thread" = Relationship(back_populates="steps")
    scores: Optional[List["Score"]] = Relationship(
        back_populates="step",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    thread: "Thread" = Relationship(back_populates="steps")

    class Config:
        arbitrary_types_allowed = True
