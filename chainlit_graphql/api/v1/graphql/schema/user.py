from typing import Optional
import strawberry
from strawberry import relay
from .role import Role


@strawberry.type
class UserType(relay.Node):
    id: relay.NodeID[int]
    email: Optional[str]
    image: Optional[str]
    name: Optional[str]
    role: Role


@strawberry.input
class RegisterInput:
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    image: Optional[str]
