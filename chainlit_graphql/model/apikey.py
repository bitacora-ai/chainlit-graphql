from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class ApiKey(SQLModel, table=True):
    __tablename__ = "apikeys"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    key: str = None
    name: str = None
    user_id: int = Field(default=None, foreign_key="users.id")
    project_id: str
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "single_parent": True}
    )
