from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .apikey import ApiKey


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(None, primary_key=True, nullable=False)
    email: str = Field(unique=True, index=True)
    password: str
    image: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = "OWNER"
    createdAt: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False)
    )
    apikeys: List["ApiKey"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    class Config:
        arbitrary_types_allowed = True
