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

    type_: types.Literal[
        helpers.property_.type_.Type.SIMPLE,
        helpers.property_.type_.Type.JSON,
        helpers.property_.type_.Type.RELATIONSHIP,
        helpers.property_.type_.Type.BACKREF,
    ]
    schema: typing.Union[
        types.Schema,
        types.ColumnSchema,
        types.ObjectRefSchema,
        types.ArrayRefSchema,
    ]
    required: typing.Optional[bool]


class _OpenApiSimplePropertyTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the OpenAPI artifacts for a simple property."""

    format_: str
    max_length: int
    nullable: bool

    description: str

    default: typing.Union[int, float, str, bool]

    read_only: bool
    write_only: bool


class OpenApiSimplePropertyTypedDict(_OpenApiSimplePropertyTypedDictBase, total=True):
    """TypedDict representation of the OpenAPI artifacts for a simple property."""

    type: str


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

    def to_dict(self) -> OpenApiSimplePropertyTypedDict:
        """Convert to dictionary."""
        return_dict: OpenApiSimplePropertyTypedDict = {"type": self.type_}

        opt_keys: typing.List[
            types.Literal[
                "format_",
                "max_length",
                "nullable",
                "description",
                "default",
                "read_only",
                "write_only",
            ]
        ] = [
            "format_",
            "max_length",
            "nullable",
            "description",
            "default",
            "read_only",
            "write_only",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


class _ExtensionSimplePropertyTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the extension artifacts for a simple property."""

    autoincrement: bool
    index: bool
    unique: bool

    foreign_key: str

    kwargs: TKwargs
    foreign_key_kwargs: TKwargs


class ExtensionSimplePropertyTypedDict(
    _ExtensionSimplePropertyTypedDictBase, total=True
):
    """TypedDict representation of the extension artifacts for a simple property."""

    primary_key: bool


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

    def to_dict(self) -> ExtensionSimplePropertyTypedDict:
        """Convert to dictionary."""
        return_dict: ExtensionSimplePropertyTypedDict = {
            "primary_key": self.primary_key
        }

        opt_keys: typing.List[
            types.Literal[
                "autoincrement",
                "index",
                "unique",
                "foreign_key",
                "kwargs",
                "foreign_key_kwargs",
            ]
        ] = [
            "autoincrement",
            "index",
            "unique",
            "foreign_key",
            "kwargs",
            "foreign_key_kwargs",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


class SimplePropertyTypedDict(types.TypedDict, total=True):
    """TypedDict representation of the simple property."""

    type: str
    open_api: OpenApiSimplePropertyTypedDict
    extension: ExtensionSimplePropertyTypedDict
    schema: types.ColumnSchema
    required: bool


@dataclasses.dataclass
class SimplePropertyArtifacts(PropertyArtifacts):
    """Information about a simple property."""

    type_: types.Literal[helpers.property_.type_.Type.SIMPLE]
    open_api: OpenApiSimplePropertyArtifacts
    extension: ExtensionSimplePropertyArtifacts
    schema: types.ColumnSchema
    required: bool

    def to_dict(self) -> SimplePropertyTypedDict:
        """Convert to dictionary."""
        return {
            "type": self.type_,
            "open_api": self.open_api.to_dict(),
            "extension": self.extension.to_dict(),
            "schema": self.schema,
            "required": self.required,
        }


class OpenApiJsonPropertyTypedDict(types.TypedDict, total=False):
    """TypedDict representation of the OpenAPI artifacts for a JSON property."""

    nullable: bool

    description: str

    read_only: bool
    write_only: bool


@dataclasses.dataclass
class OpenApiJsonPropertyArtifacts:
    """OpenAPI artifacts for the JSON property."""

    nullable: typing.Optional[bool]

    description: typing.Optional[str]

    read_only: typing.Optional[bool]
    write_only: typing.Optional[bool]

    def to_dict(self) -> OpenApiJsonPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: OpenApiJsonPropertyTypedDict = {}

        opt_keys: typing.List[
            types.Literal["nullable", "description", "read_only", "write_only"]
        ] = [
            "nullable",
            "description",
            "read_only",
            "write_only",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


class _ExtensionJsonPropertyTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the extension artifacts for a JSON property."""

    index: bool
    unique: bool

    foreign_key: str

    kwargs: TKwargs
    foreign_key_kwargs: TKwargs


class ExtensionJsonPropertyTypedDict(_ExtensionJsonPropertyTypedDictBase, total=True):
    """TypedDict representation of the extension artifacts for a JSON property."""

    primary_key: bool


@dataclasses.dataclass
class ExtensionJsonPropertyArtifacts:
    """OpenAPI artifacts for the JSON property."""

    primary_key: bool
    index: typing.Optional[bool]
    unique: typing.Optional[bool]

    foreign_key: typing.Optional[str]

    kwargs: typing.Optional[TKwargs]
    foreign_key_kwargs: typing.Optional[TKwargs]

    def to_dict(self) -> ExtensionJsonPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: ExtensionJsonPropertyTypedDict = {"primary_key": self.primary_key}

        opt_keys: typing.List[
            types.Literal[
                "index",
                "unique",
                "foreign_key",
                "kwargs",
                "foreign_key_kwargs",
            ]
        ] = [
            "index",
            "unique",
            "foreign_key",
            "kwargs",
            "foreign_key_kwargs",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


class JsonPropertyTypedDict(types.TypedDict, total=True):
    """TypedDict representation of the JSON property."""

    type: str
    open_api: OpenApiJsonPropertyTypedDict
    extension: ExtensionJsonPropertyTypedDict
    schema: types.Schema
    required: bool


@dataclasses.dataclass
class JsonPropertyArtifacts(PropertyArtifacts):
    """Information about a JSON property."""

    type_: types.Literal[helpers.property_.type_.Type.JSON]
    open_api: OpenApiJsonPropertyArtifacts
    extension: ExtensionJsonPropertyArtifacts
    schema: types.Schema
    required: bool

    def to_dict(self) -> JsonPropertyTypedDict:
        """Convert to dictionary."""
        return {
            "type": self.type_,
            "open_api": self.open_api.to_dict(),
            "extension": self.extension.to_dict(),
            "schema": self.schema,
            "required": self.required,
        }


@dataclasses.dataclass
class RelationshipPropertyArtifacts(PropertyArtifacts):
    """Information about a relationship property."""

    type_: types.Literal[helpers.property_.type_.Type.RELATIONSHIP]
    sub_type: types.Literal[
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
    required: bool


@dataclasses.dataclass
class NotManyToManyRelationshipPropertyArtifacts(RelationshipPropertyArtifacts):
    """Information about a relationship that is not many-to-many property."""

    sub_type: types.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_MANY,
    ]
    foreign_key: str
    foreign_key_property: str


class _OneToManyRelationshipPropertyTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the one-to-many relationship property."""

    backref_property: str
    kwargs: TKwargs
    write_only: bool
    description: str


class OneToManyRelationshipPropertyTypedDict(
    _OneToManyRelationshipPropertyTypedDictBase, total=True
):
    """TypedDict representation of the one-to-many relationship property."""

    type: str
    sub_type: str
    parent: str
    required: bool
    schema: types.ArrayRefSchema
    foreign_key: str
    foreign_key_property: str


@dataclasses.dataclass
class OneToManyRelationshipPropertyArtifacts(
    NotManyToManyRelationshipPropertyArtifacts
):
    """Information about a one-to-many relationship property."""

    sub_type: types.Literal[
        oa_helpers.relationship.Type.ONE_TO_MANY,
    ]
    schema: types.ArrayRefSchema

    def to_dict(self) -> OneToManyRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: OneToManyRelationshipPropertyTypedDict = {
            "type": self.type_,
            "sub_type": self.sub_type,
            "parent": self.parent,
            "required": self.required,
            "schema": self.schema,
            "foreign_key": self.foreign_key,
            "foreign_key_property": self.foreign_key_property,
        }

        opt_keys: typing.List[
            types.Literal["backref_property", "kwargs", "write_only", "description"]
        ] = [
            "backref_property",
            "kwargs",
            "write_only",
            "description",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


class _XToOneRelationshipPropertyTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the x-to-one relationship property."""

    backref_property: str
    kwargs: TKwargs
    write_only: bool
    description: str
    nullable: bool


class XToOneRelationshipPropertyTypedDict(
    _XToOneRelationshipPropertyTypedDictBase, total=True
):
    """TypedDict representation of the x-to-one relationship property."""

    type: str
    sub_type: str
    parent: str
    required: bool
    schema: types.ObjectRefSchema
    foreign_key: str
    foreign_key_property: str


@dataclasses.dataclass
class XToOneRelationshipPropertyArtifacts(NotManyToManyRelationshipPropertyArtifacts):
    """Information about a x-to-one relationship property."""

    sub_type: types.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
        oa_helpers.relationship.Type.ONE_TO_ONE,
    ]
    schema: types.ObjectRefSchema
    nullable: typing.Optional[bool]

    def to_dict(self) -> XToOneRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: XToOneRelationshipPropertyTypedDict = {
            "type": self.type_,
            "sub_type": self.sub_type,
            "parent": self.parent,
            "required": self.required,
            "schema": self.schema,
            "foreign_key": self.foreign_key,
            "foreign_key_property": self.foreign_key_property,
        }

        opt_keys: typing.List[
            types.Literal[
                "backref_property",
                "kwargs",
                "write_only",
                "description",
                "nullable",
            ]
        ] = [
            "backref_property",
            "kwargs",
            "write_only",
            "description",
            "nullable",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


ManyToOneRelationshipPropertyTypedDict = XToOneRelationshipPropertyTypedDict


@dataclasses.dataclass
class ManyToOneRelationshipPropertyArtifacts(XToOneRelationshipPropertyArtifacts):
    """Information about a many-to-one relationship property."""

    sub_type: types.Literal[
        oa_helpers.relationship.Type.MANY_TO_ONE,
    ]

    def to_dict(  # pylint: disable=useless-super-delegation
        self,
    ) -> ManyToOneRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return super().to_dict()


OneToOneRelationshipPropertyTypedDict = XToOneRelationshipPropertyTypedDict


@dataclasses.dataclass
class OneToOneRelationshipPropertyArtifacts(XToOneRelationshipPropertyArtifacts):
    """Information about a one-to-one relationship property."""

    sub_type: types.Literal[
        oa_helpers.relationship.Type.ONE_TO_ONE,
    ]

    def to_dict(  # pylint: disable=useless-super-delegation
        self,
    ) -> OneToOneRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return super().to_dict()


class _ManyToManyRelationshipPropertyTypedDictBase(types.TypedDict, total=False):
    """TypedDict representation of the many-to-many relationship property."""

    backref_property: str
    kwargs: TKwargs
    write_only: bool
    description: str


class ManyToManyRelationshipPropertyTypedDict(
    _ManyToManyRelationshipPropertyTypedDictBase, total=True
):
    """TypedDict representation of the many-to-many relationship property."""

    type: str
    sub_type: str
    parent: str
    required: bool
    schema: types.ArrayRefSchema
    secondary: str


@dataclasses.dataclass
class ManyToManyRelationshipPropertyArtifacts(RelationshipPropertyArtifacts):
    """Information about a x-to-one relationship property."""

    sub_type: types.Literal[
        oa_helpers.relationship.Type.MANY_TO_MANY,
    ]
    secondary: str
    schema: types.ArrayRefSchema

    def to_dict(self) -> ManyToManyRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: ManyToManyRelationshipPropertyTypedDict = {
            "type": self.type_,
            "sub_type": self.sub_type,
            "parent": self.parent,
            "required": self.required,
            "schema": self.schema,
            "secondary": self.secondary,
        }

        opt_keys: typing.List[
            types.Literal["backref_property", "kwargs", "write_only", "description"]
        ] = [
            "backref_property",
            "kwargs",
            "write_only",
            "description",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


TAnyRelationshipPropertyTypedDict = typing.Union[
    ManyToOneRelationshipPropertyTypedDict,
    OneToOneRelationshipPropertyTypedDict,
    OneToManyRelationshipPropertyTypedDict,
    ManyToManyRelationshipPropertyTypedDict,
]
TAnyRelationshipPropertyArtifacts = typing.Union[
    ManyToOneRelationshipPropertyArtifacts,
    OneToOneRelationshipPropertyArtifacts,
    OneToManyRelationshipPropertyArtifacts,
    ManyToManyRelationshipPropertyArtifacts,
]


class BackrefPropertyTypedDict(types.TypedDict, total=True):
    """TypedDict representation of the many-to-many relationship property."""

    type: str
    sub_type: str
    properties: typing.List[str]
    schema: types.Schema


@enum.unique
class BackrefSubType(str, enum.Enum):
    """The possible types of backreferences."""

    OBJECT = "OBJECT"
    ARRAY = "ARRAY"


@dataclasses.dataclass
class BackrefPropertyArtifacts(PropertyArtifacts):
    """Information about a back reference property."""

    type_: types.Literal[helpers.property_.type_.Type.BACKREF]
    sub_type: types.Literal[BackrefSubType.OBJECT, BackrefSubType.ARRAY]
    properties: typing.List[str]
    schema: types.Schema
    required: None

    def to_dict(self) -> BackrefPropertyTypedDict:
        """Convert to dictionary."""
        return {
            "type": self.type_,
            "sub_type": self.sub_type,
            "properties": self.properties,
            "schema": self.schema,
        }


TAnyPropertyTypedDict = typing.Union[
    SimplePropertyTypedDict,
    JsonPropertyTypedDict,
    TAnyRelationshipPropertyTypedDict,
    BackrefPropertyTypedDict,
]
TAnyPropertyArtifacts = typing.Union[
    SimplePropertyArtifacts,
    JsonPropertyArtifacts,
    TAnyRelationshipPropertyArtifacts,
    BackrefPropertyArtifacts,
]


class TProperty(types.TypedDict, total=True):
    """Artifacts for a property."""

    artifacts: TAnyPropertyTypedDict


TProperties = typing.Dict[str, TProperty]


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


class _TModelBase(types.TypedDict, total=False):
    """Record artifacts of a model."""

    properties: TProperties


class TModel(_TModelBase, total=True):
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
            types.Literal[
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
