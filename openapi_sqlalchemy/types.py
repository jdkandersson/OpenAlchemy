"""Types shared across modules."""

import dataclasses
import typing

SchemaSpec = typing.Dict[str, typing.Any]
Schemas = typing.Dict[str, SchemaSpec]


@dataclasses.dataclass
class Schema:
    """Schema for a table."""

    logical_name: str
    spec: SchemaSpec
