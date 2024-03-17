from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy import Column, DateTime, String, JSON, ARRAY
from sqlalchemy.sql import func
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .participant import Participant
    from .step import Step


class Thread(SQLModel, table=True):
    __tablename__ = "threads"

    # Existing fields
    id: Optional[str] = Field(sa_column=Column(String, primary_key=True, index=True))
    name: Optional[str]
    meta_data: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    environment: Optional[str]
    tags: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)), default=[])
    createdAt: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False)
    )
    participant_id: Optional[str] = Field(
        default=None, foreign_key="participants.id"
    )  # Foreign key to Participant
    participant: "Participant" = Relationship(back_populates="threads")
    steps: List["Step"] = Relationship(
        back_populates="thread",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    class Config:
        arbitrary_types_allowed = True
