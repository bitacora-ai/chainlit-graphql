from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy import Column, DateTime, JSON
from sqlalchemy.sql import func
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .thread import Thread


class Participant(SQLModel, table=True):
    __tablename__ = "participants"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    identifier: Optional[str] = None
    meta_data: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    createdAt: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False)
    )
    threads: List["Thread"] = Relationship(
        back_populates="participant", sa_relationship_kwargs={"lazy": "selectin"}
    )

    class Config:
        arbitrary_types_allowed = True
