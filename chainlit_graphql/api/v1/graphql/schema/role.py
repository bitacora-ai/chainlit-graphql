import strawberry
from enum import Enum


@strawberry.enum
class Role(Enum):
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    USER = "USER"
