import strawberry
from typing import NewType, Any

Json = strawberry.scalar(
    NewType("Json", object),
    description="The `Json` scalar type represents JSON values as specified by ECMA-404",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)


# Correctly define serialization and parsing functions for the custom scalar
def serialize_unknown(value: Any) -> str:
    # Here, you would serialize your Python object to a string
    # For simplicity, let's just convert it to a string representation
    return str(value)


def parse_unknown(value: str) -> Any:
    # Here, you would parse the string back to a Python object
    # For simplicity, let's return the value directly, assuming it's already the correct type
    return value


# Define the custom scalar in Strawberry
Unknown = strawberry.scalar(
    NewType("Unknown", object),
    serialize=serialize_unknown,
    parse_value=parse_unknown,
    name="Unknown",
    description="A custom scalar for handling arbitrary JSON data.",
)
