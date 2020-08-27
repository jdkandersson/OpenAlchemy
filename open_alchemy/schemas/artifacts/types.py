"""The artifact types."""

import dataclasses
import enum
import typing

from ... import helpers as oa_helpers
from ... import types
from .. import helpers

TMixins = typing.List[str]
TKwargs = typing.Dict[str, typing.Any]


@dataclasses.dataclass
class PropertyArtifacts:
    """Information about a property."""

    type_: typing.Literal[
        helpers.property_.type_.Type.SIMPLE,
        helpers.property_.type_.Type.JSON,
        helpers.property_.type_.Type.RELATIONSHIP,
        helpers.property_.type_.Type.BACKREF,
    ]
    schema: typing.Optional[
        typing.Union[
            types.Schema,
            types.ColumnSchema,
            types.ObjectRefSchema,
            types.ArrayRefSchema,
        ]
    ]
    required: typing.Optional[bool]


@dataclasses.dataclass
class OpenApiSimplePropertyArtifacts:
    """OpenAPI artifacts for the simple property."""

    type_: str
    format_: typing.Optional[str]
    max_length: typing.Optional[int]
    nullable: typing.Optional[bool]

    description: typing.Optional[str]

    default: typing.Optional[typing.Union[int, float, str, bool]]

    read_only: typing.Optional[bool]
    write_only: typing.Optional[bool]


@dataclasses.dataclass
class ExtensionSimplePropertyArtifacts:
    """OpenAPI artifacts for the simple property."""

    primary_key: bool
    autoincrement: typing.Optional[bool]
    index: typing.Optional[bool]
    unique: typing.Optional[bool]

    foreign_key: typing.Optional[str]

    kwargs: typing.Optional[TKwargs]
    foreign_key_kwargs: typing.Optional[TKwargs]


@dataclasses.dataclass
class SimplePropertyArtifacts(PropertyArtifacts):
    """Information about a simple property."""

    type_: typing.Literal[helpers.property_.type_.Type.SIMPLE]
    open_api: OpenApiSimplePropertyArtifacts
    extension: ExtensionSimplePropertyArtifacts
    schema: types.ColumnSchema


@dataclasses.dataclass
class OpenApiJsonPropertyArtifacts:
    """OpenAPI artifacts for the JSON property."""

    nullable: typing.Optional[bool]

    description: typing.Optional[str]

    read_only: typing.Optional[bool]
    write_only: typing.Optional[bool]


@dataclasses.dataclass
class ExtensionJsonPropertyArtifacts:
    """OpenAPI artifacts for the JSON property."""

    primary_key: bool
    index: typing.Optional[bool]
    unique: typing.Optional[bool]

    foreign_key: typing.Optional[str]

    kwargs: typing.Optional[TKwargs]
    foreign_key_kwargs: typing.Optional[TKwargs]


@dataclasses.dataclass
class JsonPropertyArtifacts(PropertyArtifacts):
    """Information about a JSON property."""

    type_: typing.Literal[helpers.property_.type_.Type.JSON]
    open_api: OpenApiJsonPropertyArtifacts
    extension: ExtensionJsonPropertyArtifacts
    schema: types.Schema


@dataclasses.dataclass
class RelationshipPropertyArtifacts(PropertyArtifacts):
    """Information about a relationship property."""

    type_: typing.Literal[helpers.property_.type_.Type.RELATIONSHIP]
    sub_type: typing.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_MANY,
        oa_helpers.relationship.Type.MANY_TO_MANY,
    ]
    parent: str
    backref_property: typing.Optional[str]
    kwargs: typing.Optional[TKwargs]
    write_only: typing.Optional[bool]
    description: typing.Optional[str]


@dataclasses.dataclass
class NotManyToManyRelationshipPropertyArtifacts(RelationshipPropertyArtifacts):
    """Information about a relationship that is not many-to-many property."""

    sub_type: typing.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_MANY,
    ]
    foreign_key: str
    foreign_key_property: str


@dataclasses.dataclass
class OneToManyRelationshipPropertyArtifacts(
    NotManyToManyRelationshipPropertyArtifacts
):
    """Information about a one-to-many relationship property."""

    sub_type: typing.Literal[
        oa_helpers.relationship.Type.ONE_TO_MANY,
    ]
    schema: types.ArrayRefSchema


@dataclasses.dataclass
class XToOneRelationshipPropertyArtifacts(NotManyToManyRelationshipPropertyArtifacts):
    """Information about a x-to-one relationship property."""

    sub_type: typing.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_ONE,
    ]
    nullable: typing.Optional[bool]


@dataclasses.dataclass
class ManyToOneRelationshipPropertyArtifacts(XToOneRelationshipPropertyArtifacts):
    """Information about a many-to-one relationship property."""

    sub_type: typing.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
    ]
    schema: types.ObjectRefSchema


@dataclasses.dataclass
class OneToOneRelationshipPropertyArtifacts(XToOneRelationshipPropertyArtifacts):
    """Information about a one-to-one relationship property."""

    sub_type: typing.Literal[
        oa_helpers.relationship.Type.ONE_TO_ONE,
    ]
    schema: types.ObjectRefSchema


@dataclasses.dataclass
class ManyToManyRelationshipPropertyArtifacts(RelationshipPropertyArtifacts):
    """Information about a x-to-one relationship property."""

    sub_type: typing.Literal[
        oa_helpers.relationship.Type.MANY_TO_MANY,
    ]
    secondary: str
    schema: types.ArrayRefSchema


TAnyRelationshipPropertyArtifacts = typing.Union[
    ManyToOneRelationshipPropertyArtifacts,
    OneToOneRelationshipPropertyArtifacts,
    OneToManyRelationshipPropertyArtifacts,
    ManyToManyRelationshipPropertyArtifacts,
]


class BackrefSubType(enum.Enum):
    """The possible types of backreferences."""

    OBJECT = 1
    ARRAY = 2


@dataclasses.dataclass
class BackrefPropertyArtifacts(PropertyArtifacts):
    """Information about a back reference property."""

    type_: typing.Literal[helpers.property_.type_.Type.BACKREF]
    sub_type: typing.Literal[BackrefSubType.OBJECT, BackrefSubType.ARRAY]
    properties: typing.List[str]
    schema: types.Schema


class _ModelTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the model artifacts."""

    inherits: bool
    parent: str

    description: str

    mixins: TMixins

    kwargs: TKwargs

    composite_index: types.IndexList
    composite_unique: types.UniqueList


class ModelTypedDict(_ModelTypedDictBase, total=True):
    """TypedDict representation of the model artifacts."""

    tablename: str


class TModel(types.TypedDict, total=True):
    """Record artifacts of a model."""

    artifacts: ModelTypedDict


@dataclasses.dataclass
class ModelArtifacts:
    """Information about a model."""

    tablename: str
    inherits: typing.Optional[bool]
    parent: typing.Optional[str]

    description: typing.Optional[str]

    mixins: typing.Optional[TMixins]

    kwargs: typing.Optional[TKwargs]

    composite_index: typing.Optional[types.IndexList]
    composite_unique: typing.Optional[types.UniqueList]

    def to_dict(self) -> ModelTypedDict:
        """Convert to dictionary."""
        return_dict: ModelTypedDict = {"tablename": self.tablename}

        opt_keys: typing.List[
            typing.Literal[
                "inherits",
                "parent",
                "description",
                "mixins",
                "kwargs",
                "composite_index",
                "composite_unique",
            ]
        ] = [
            "inherits",
            "parent",
            "description",
            "mixins",
            "kwargs",
            "composite_index",
            "composite_unique",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


TModels = typing.Dict[str, TModel]


class TSpec(types.TypedDict, total=False):
    """Record artifacts for a specification."""

    models: TModels
