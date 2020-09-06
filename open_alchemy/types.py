"""Types shared across modules."""

import dataclasses
import datetime
import typing

try:  # pragma: no cover
    from typing import Literal
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


_ColumnSchemaBase = TypedDict(  # pylint: disable=invalid-name
    "_ColumnSchemaBase",
    {
        "x-dict-ignore": bool,
        "format": str,
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


@dataclasses.dataclass
class OpenAPiColumnArtifacts:
    """OpenAPI information required to construct a column."""

    type: str
    format: typing.Optional[str] = None
    max_length: typing.Optional[int] = None
    nullable: bool = True
    description: typing.Optional[str] = None
    default: TColumnDefault = None
    read_only: typing.Optional[bool] = None
    write_only: typing.Optional[bool] = None


@dataclasses.dataclass
class ExtensionColumnArtifacts:
    """Extension property information required to construct a column."""

    primary_key: typing.Optional[bool] = None
    autoincrement: typing.Optional[bool] = None
    index: typing.Optional[bool] = None
    unique: typing.Optional[bool] = None
    json: typing.Optional[bool] = None
    foreign_key: typing.Optional[str] = None
    foreign_key_kwargs: TOptKwargs = None
    kwargs: TOptKwargs = None


@dataclasses.dataclass
class ColumnArtifacts:
    """Information required to construct a column."""

    open_api: OpenAPiColumnArtifacts
    extension: ExtensionColumnArtifacts

    def __init__(
        self,
        open_api: OpenAPiColumnArtifacts,
        extension: typing.Optional[ExtensionColumnArtifacts] = None,
    ) -> None:
        """Construct."""
        self.open_api = open_api
        if extension is None:
            extension = ExtensionColumnArtifacts()
        self.extension = extension


@dataclasses.dataclass
class BackReferenceArtifacts:
    """Information required to construct a back reference."""

    # The property name under which to make the back reference available
    property_name: str
    # Whether to use a list
    uselist: typing.Optional[bool] = None


@dataclasses.dataclass
class RelationshipArtifacts:
    """Information required to construct a relationship to another model."""

    # The name of the referenced model
    model_name: str
    # Information for the optional back reference
    back_reference: typing.Optional[BackReferenceArtifacts] = None
    # The name of the optional secondary table to use
    secondary: typing.Optional[str] = None
    # Keyword arguments for the relationship construction
    kwargs: TOptKwargs = None


@dataclasses.dataclass
class ObjectArtifacts:
    """Artifacts retrieved from object schema."""

    spec: Schema
    logical_name: str
    fk_column: str
    relationship: RelationshipArtifacts
    nullable: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    write_only: typing.Optional[bool] = None


_ObjectRefSchemaBase = TypedDict(  # pylint: disable=invalid-name
    "_ObjectRefSchemaBase", {"type": str, "x-de-$ref": str}, total=True
)


class ObjectRefSchema(_ObjectRefSchemaBase, total=False):
    """Schema for object reference definitions."""

    nullable: bool
    description: str
    readOnly: bool
    writeOnly: bool


_ArrayRefSchemaBase = TypedDict(  # pylint: disable=invalid-name
    "_ArrayRefSchemaBase",
    {"description": str, "readOnly": bool, "writeOnly": bool},
    total=False,
)


class ArrayRefSchema(_ArrayRefSchemaBase, total=True):
    """Schema for array reference definitions."""

    type: str
    items: _ObjectRefSchemaBase


_ReadOnlySchemaBase = TypedDict(  # pylint: disable=invalid-name
    "_ReadOnlySchemaBase", {"readOnly": bool}, total=True
)


class ReadOnlySchemaObjectCommon(TypedDict, total=True):
    """Base class for object schema."""

    type: Literal["object"]
    properties: Schema


class ReadOnlyObjectSchema(ReadOnlySchemaObjectCommon, _ReadOnlySchemaBase):
    """Base class for object readOnly schema."""


class ReadOnlyArraySchema(_ReadOnlySchemaBase):
    """Base class for object readOnly schema."""

    type: Literal["array"]
    items: ReadOnlySchemaObjectCommon


ReadOnlySchema = typing.Union[ReadOnlyObjectSchema, ReadOnlyArraySchema]
