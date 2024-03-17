import strawberry
from typing import NewType

Json = strawberry.scalar(
    NewType("Json", object),
    description="The `Json` scalar type represents JSON values as specified by ECMA-404",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
