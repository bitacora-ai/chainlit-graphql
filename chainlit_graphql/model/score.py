from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import Column, JSON
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .step import Step


class Score(SQLModel, table=True):
    __tablename__ = "scores"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    name: Optional[str]
    type: Optional[str]
    value: Optional[float]
    comment: Optional[str] = None
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    step_id: Optional[str] = Field(default=None, foreign_key="steps.id")
    generation_id: Optional[str] = None
    dataset_experiment_item_id: Optional[str] = None

    step: Optional["Step"] = Relationship(back_populates="scores")
