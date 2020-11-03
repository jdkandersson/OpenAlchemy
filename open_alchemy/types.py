"""Types shared across modules."""

import datetime
import typing

try:  # pragma: no cover
    from typing import Literal  # pylint: disable=unused-import
    from typing import Protocol
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore
    from typing_extensions import Protocol  # type: ignore
    from typing_extensions import TypedDict  # type: ignore

Schema = typing.Dict[str, typing.Any]
Schemas = typing.Dict[str, Schema]
AllOfSpec = typing.List[Schema]
TKwargs = typing.Dict[str, typing.Any]
TOptKwargs = typing.Optional[TKwargs]


class ModelFactory(Protocol):
    """Defines interface for model factory."""

    def __call__(self, *, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...


class GetBase(Protocol):
    """Defines interface for the get_base function."""

    def __call__(self, *, name: str, schemas: Schemas) -> typing.Type:
        """Call signature for get_base."""
        ...


# Unique consraint types
ColumnList = typing.List[str]
ColumnListList = typing.List[ColumnList]


class _UniqueBase(TypedDict, total=True):
    """Base class for unique schema."""

    columns: typing.List[str]


class Unique(_UniqueBase, total=False):
    """Unique schema."""

    name: typing.Optional[str]


UniqueList = typing.List[Unique]
AnyUnique = typing.Union[ColumnList, ColumnListList, Unique, UniqueList]
# Index types


class _IndexBase(TypedDict, total=True):
    """Base class for index schema."""

    expressions: typing.List[str]


class Index(_IndexBase, total=False):
    """Index schema."""

    name: typing.Optional[str]
    unique: bool


IndexList = typing.List[Index]
AnyIndex = typing.Union[ColumnList, ColumnListList, Index, IndexList]
# Type for the default value
TColumnDefault = typing.Optional[typing.Union[str, int, float, bool]]
# Type for the default value expressed in Python
TPyColumnDefault = typing.Optional[
    typing.Union[str, int, float, bool, bytes, datetime.date, datetime.datetime]
]


_ColumnSchemaBase = TypedDict(
    "_ColumnSchemaBase",
    {
        "x-dict-ignore": bool,
        "format": str,
        "x-primary-key": bool,
        "maxLength": int,
        "nullable": bool,
        "description": str,
        "x-json": bool,
        "default": TColumnDefault,
        "x-generated": bool,
        "readOnly": bool,
        "writeOnly": bool,
        "x-foreign-key": str,
    },
    total=False,
)


class ColumnSchema(_ColumnSchemaBase, total=True):
    """Schema for column definitions."""

    type: str


_ObjectRefSchemaBase = TypedDict(
    "_ObjectRefSchemaBase", {"type": str, "x-de-$ref": str}, total=True
)


class ObjectRefSchema(_ObjectRefSchemaBase, total=False):
    """Schema for object reference definitions."""

    nullable: bool
    description: str
    readOnly: bool
    writeOnly: bool


_ArrayRefSchemaBase = TypedDict(
    "_ArrayRefSchemaBase",
    {"description": str, "readOnly": bool, "writeOnly": bool},
    total=False,
)


class ArrayRefSchema(_ArrayRefSchemaBase, total=True):
    """Schema for array reference definitions."""

    type: str
    items: _ObjectRefSchemaBase


class TNameSchema(typing.NamedTuple):
    """The name and schema of a schema."""

    name: str
    schema: Schema
