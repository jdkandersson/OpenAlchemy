"""Types shared across modules."""

import dataclasses
import datetime
import enum
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
TKwargs = typing.Dict[str, typing.Any]
TOptKwargs = typing.Optional[TKwargs]


@enum.unique
class KeyPrefixes(str, enum.Enum):
    """The allowed prefixes for extension properties."""

    SHORT = "x-"
    NAMESPACES = "x-open-alchemy-"


@enum.unique
class OpenApiProperties(str, enum.Enum):
    """All the OpenAPI properties that can be defined."""

    TYPE: Literal["type"] = "type"
    NULLABLE: Literal["nullable"] = "nullable"
    FORMAT: Literal["format"] = "format"
    MAX_LENGTH: Literal["maxLength"] = "maxLength"
    READ_ONLY: Literal["readOnly"] = "readOnly"
    WRITE_ONLY: Literal["writeOnly"] = "writeOnly"
    DESCRIPTION: Literal["description"] = "description"
    ITEMS: Literal["items"] = "items"
    REF: Literal["$ref"] = "$ref"
    DEFAULT: Literal["default"] = "default"
    REQUIRED: Literal["required"] = "required"
    PROPERTIES: Literal["properties"] = "properties"


@enum.unique
class ExtensionProperties(str, enum.Enum):
    """All the extension properties that can be defined."""

    AUTOINCREMENT: Literal["x-autoincrement"] = "x-autoincrement"
    INDEX: Literal["x-index"] = "x-index"
    UNIQUE: Literal["x-unique"] = "x-unique"
    PRIMARY_KEY: Literal["x-primary-key"] = "x-primary-key"
    TABLENAME: Literal["x-tablename"] = "x-tablename"
    INHERITS: Literal["x-inherits"] = "x-inherits"
    JSON: Literal["x-json"] = "x-json"
    BACKREF: Literal["x-backref"] = "x-backref"
    SECONDARY: Literal["x-secondary"] = "x-secondary"
    USELIST: Literal["x-uselist"] = "x-uselist"
    KWARGS: Literal["x-kwargs"] = "x-kwargs"
    FOREIGN_KEY_KWARGS: Literal["x-foreign-key-kwargs"] = "x-foreign-key-kwargs"
    FOREIGN_KEY: Literal["x-foreign-key"] = "x-foreign-key"
    FOREIGN_KEY_COLUMN: Literal["x-foreign-key-column"] = "x-foreign-key-column"
    COMPOSITE_INDEX: Literal["x-composite-index"] = "x-composite-index"
    COMPOSITE_UNIQUE: Literal["x-composite-unique"] = "x-composite-unique"
    SERVER_DEFAULT: Literal["x-server-default"] = "x-server-default"
    MIXINS: Literal["x-mixins"] = "x-mixins"
    DICT_IGNORE: Literal["x-dict-ignore"] = "x-dict-ignore"
    BACKREFS: Literal["x-backrefs"] = "x-backrefs"
    DE_REF: Literal["x-de-$ref"] = "x-de-$ref"


class ModelFactory(Protocol):
    """Defines interface for model factory."""

    def __call__(self, *, name: str) -> typing.Type:
        """Call signature for ModelFactory."""
        ...


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


class _IndexBase(TypedDict, total=True):
    """Base class for index schema."""

    expressions: typing.List[str]


class Index(_IndexBase, total=False):
    """Index schema."""

    name: typing.Optional[str]
    unique: bool


IndexList = typing.List[Index]
AnyIndex = typing.Union[ColumnList, ColumnListList, Index, IndexList]
TColumnDefault = typing.Optional[typing.Union[str, int, float, bool]]
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
        "x-server-default": str,
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


@enum.unique
class PropertyType(str, enum.Enum):
    """The type of a property."""

    SIMPLE = "SIMPLE"
    JSON = "JSON"
    RELATIONSHIP = "RELATIONSHIP"
    BACKREF = "BACKREF"


@enum.unique
class RelationshipType(str, enum.Enum):
    """The relationship type."""

    MANY_TO_ONE = "MANY_TO_ONE"
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"


TMixins = typing.List[str]


@dataclasses.dataclass
class PropertyArtifacts:
    """Information about a property."""

    type: Literal[
        PropertyType.SIMPLE,
        PropertyType.JSON,
        PropertyType.RELATIONSHIP,
        PropertyType.BACKREF,
    ]
    schema: typing.Union[
        Schema,
        ColumnSchema,
        ObjectRefSchema,
        ArrayRefSchema,
    ]
    required: typing.Optional[bool]
    description: typing.Optional[str]


class _OpenApiSimplePropertyTypedDictBase(TypedDict, total=False):
    """TypedDict representation of the OpenAPI artifacts for a simple property."""

    format: str
    max_length: int
    nullable: bool
    default: typing.Union[int, float, str, bool]
    read_only: bool
    write_only: bool


class OpenApiSimplePropertyTypedDict(_OpenApiSimplePropertyTypedDictBase, total=True):
    """TypedDict representation of the OpenAPI artifacts for a simple property."""

    type: str


@dataclasses.dataclass
class OpenApiSimplePropertyArtifacts:
    """OpenAPI artifacts for the simple property."""

    type: str
    format: typing.Optional[str]
    max_length: typing.Optional[int]
    nullable: typing.Optional[bool]
    default: typing.Optional[typing.Union[int, float, str, bool]]
    read_only: typing.Optional[bool]
    write_only: typing.Optional[bool]

    def to_dict(self) -> OpenApiSimplePropertyTypedDict:
        """Convert to dictionary."""
        return_dict: OpenApiSimplePropertyTypedDict = {"type": self.type}

        opt_keys: typing.List[
            Literal[
                "format",
                "max_length",
                "nullable",
                "default",
                "read_only",
                "write_only",
            ]
        ] = [
            "format",
            "max_length",
            "nullable",
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


class _ExtensionSimplePropertyTypedDictBase(TypedDict, total=False):
    """TypedDict representation of the extension artifacts for a simple property."""

    autoincrement: bool
    index: bool
    unique: bool
    server_default: str
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
    server_default: typing.Optional[str]
    foreign_key: typing.Optional[str]
    kwargs: typing.Optional[TKwargs]
    foreign_key_kwargs: typing.Optional[TKwargs]
    dict_ignore: typing.Optional[bool]

    def to_dict(self) -> ExtensionSimplePropertyTypedDict:
        """Convert to dictionary."""
        return_dict: ExtensionSimplePropertyTypedDict = {
            "primary_key": self.primary_key
        }

        opt_keys: typing.List[
            Literal[
                "autoincrement",
                "index",
                "unique",
                "server_default",
                "foreign_key",
                "kwargs",
                "foreign_key_kwargs",
            ]
        ] = [
            "autoincrement",
            "index",
            "unique",
            "server_default",
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


class _SimplePropertyTypedDictBase(TypedDict, total=False):
    """TypedDict representation of the simple property."""

    description: str


class SimplePropertyTypedDict(_SimplePropertyTypedDictBase, total=True):
    """TypedDict representation of the simple property."""

    type: str
    open_api: OpenApiSimplePropertyTypedDict
    extension: ExtensionSimplePropertyTypedDict
    schema: ColumnSchema
    required: bool


@dataclasses.dataclass
class SimplePropertyArtifacts(PropertyArtifacts):
    """Information about a simple property."""

    type: Literal[PropertyType.SIMPLE]
    open_api: OpenApiSimplePropertyArtifacts
    extension: ExtensionSimplePropertyArtifacts
    schema: ColumnSchema
    required: bool

    def to_dict(self) -> SimplePropertyTypedDict:
        """Convert to dictionary."""
        return_dict: SimplePropertyTypedDict = {
            "type": self.type,
            "open_api": self.open_api.to_dict(),
            "extension": self.extension.to_dict(),
            "schema": self.schema,
            "required": self.required,
        }

        if self.description is not None:
            return_dict["description"] = self.description

        return return_dict


class OpenApiJsonPropertyTypedDict(TypedDict, total=False):
    """TypedDict representation of the OpenAPI artifacts for a JSON property."""

    nullable: bool
    read_only: bool
    write_only: bool


@dataclasses.dataclass
class OpenApiJsonPropertyArtifacts:
    """OpenAPI artifacts for the JSON property."""

    nullable: typing.Optional[bool]

    read_only: typing.Optional[bool]
    write_only: typing.Optional[bool]

    def to_dict(self) -> OpenApiJsonPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: OpenApiJsonPropertyTypedDict = {}

        opt_keys: typing.List[Literal["nullable", "read_only", "write_only"]] = [
            "nullable",
            "read_only",
            "write_only",
        ]
        for opt_key in opt_keys:
            value = getattr(self, opt_key)
            if value is None:
                continue

            return_dict[opt_key] = value

        return return_dict


class _ExtensionJsonPropertyTypedDictBase(TypedDict, total=False):
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
            Literal[
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


class _JsonPropertyTypedDictBase(TypedDict, total=False):
    """TypedDict representation of the JSON property."""

    description: str


class JsonPropertyTypedDict(_JsonPropertyTypedDictBase, total=True):
    """TypedDict representation of the JSON property."""

    type: str
    open_api: OpenApiJsonPropertyTypedDict
    extension: ExtensionJsonPropertyTypedDict
    schema: Schema
    required: bool


@dataclasses.dataclass
class JsonPropertyArtifacts(PropertyArtifacts):
    """Information about a JSON property."""

    type: Literal[PropertyType.JSON]
    open_api: OpenApiJsonPropertyArtifacts
    extension: ExtensionJsonPropertyArtifacts
    schema: Schema
    required: bool

    def to_dict(self) -> JsonPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: JsonPropertyTypedDict = {
            "type": self.type,
            "open_api": self.open_api.to_dict(),
            "extension": self.extension.to_dict(),
            "schema": self.schema,
            "required": self.required,
        }

        if self.description is not None:
            return_dict["description"] = self.description

        return return_dict


@dataclasses.dataclass
class RelationshipPropertyArtifacts(PropertyArtifacts):
    """Information about a relationship property."""

    type: Literal[PropertyType.RELATIONSHIP]
    sub_type: Literal[
        RelationshipType.MANY_TO_ONE,
        RelationshipType.ONE_TO_ONE,
        RelationshipType.ONE_TO_MANY,
        RelationshipType.MANY_TO_MANY,
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

    sub_type: Literal[
        RelationshipType.MANY_TO_ONE,
        RelationshipType.ONE_TO_ONE,
        RelationshipType.ONE_TO_MANY,
    ]
    foreign_key: str
    foreign_key_property: str


class _OneToManyRelationshipPropertyTypedDictBase(TypedDict, total=False):
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
    schema: ArrayRefSchema
    foreign_key: str
    foreign_key_property: str


@dataclasses.dataclass
class OneToManyRelationshipPropertyArtifacts(
    NotManyToManyRelationshipPropertyArtifacts
):
    """Information about a one-to-many relationship property."""

    sub_type: Literal[
        RelationshipType.ONE_TO_MANY,
    ]
    schema: ArrayRefSchema

    def to_dict(self) -> OneToManyRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: OneToManyRelationshipPropertyTypedDict = {
            "type": self.type,
            "sub_type": self.sub_type,
            "parent": self.parent,
            "required": self.required,
            "schema": self.schema,
            "foreign_key": self.foreign_key,
            "foreign_key_property": self.foreign_key_property,
        }

        opt_keys: typing.List[
            Literal["backref_property", "kwargs", "write_only", "description"]
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


class _XToOneRelationshipPropertyTypedDictBase(TypedDict, total=False):
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
    schema: ObjectRefSchema
    foreign_key: str
    foreign_key_property: str


@dataclasses.dataclass
class XToOneRelationshipPropertyArtifacts(NotManyToManyRelationshipPropertyArtifacts):
    """Information about a x-to-one relationship property."""

    sub_type: Literal[
        RelationshipType.MANY_TO_ONE,
        RelationshipType.ONE_TO_ONE,
    ]
    schema: ObjectRefSchema
    nullable: typing.Optional[bool]

    def to_dict(self) -> XToOneRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: XToOneRelationshipPropertyTypedDict = {
            "type": self.type,
            "sub_type": self.sub_type,
            "parent": self.parent,
            "required": self.required,
            "schema": self.schema,
            "foreign_key": self.foreign_key,
            "foreign_key_property": self.foreign_key_property,
        }

        opt_keys: typing.List[
            Literal[
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

    sub_type: Literal[
        RelationshipType.MANY_TO_ONE,
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

    sub_type: Literal[
        RelationshipType.ONE_TO_ONE,
    ]

    def to_dict(  # pylint: disable=useless-super-delegation
        self,
    ) -> OneToOneRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return super().to_dict()


class _ManyToManyRelationshipPropertyTypedDictBase(TypedDict, total=False):
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
    schema: ArrayRefSchema
    secondary: str


@dataclasses.dataclass
class ManyToManyRelationshipPropertyArtifacts(RelationshipPropertyArtifacts):
    """Information about a x-to-one relationship property."""

    sub_type: Literal[
        RelationshipType.MANY_TO_MANY,
    ]
    secondary: str
    schema: ArrayRefSchema

    def to_dict(self) -> ManyToManyRelationshipPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: ManyToManyRelationshipPropertyTypedDict = {
            "type": self.type,
            "sub_type": self.sub_type,
            "parent": self.parent,
            "required": self.required,
            "schema": self.schema,
            "secondary": self.secondary,
        }

        opt_keys: typing.List[
            Literal["backref_property", "kwargs", "write_only", "description"]
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


class _BackrefPropertyTypedDictBase(TypedDict, total=False):
    """TypedDict representation of the backref property."""

    description: str


class BackrefPropertyTypedDict(_BackrefPropertyTypedDictBase, total=True):
    """TypedDict representation of the backref property."""

    type: str
    sub_type: str
    properties: typing.List[str]
    schema: Schema


@enum.unique
class BackrefSubType(str, enum.Enum):
    """The possible types of backreferences."""

    OBJECT = "OBJECT"
    ARRAY = "ARRAY"


@dataclasses.dataclass
class BackrefPropertyArtifacts(PropertyArtifacts):
    """Information about a back reference property."""

    type: Literal[PropertyType.BACKREF]
    sub_type: Literal[BackrefSubType.OBJECT, BackrefSubType.ARRAY]
    properties: typing.List[str]
    schema: Schema
    required: None

    def to_dict(self) -> BackrefPropertyTypedDict:
        """Convert to dictionary."""
        return_dict: BackrefPropertyTypedDict = {
            "type": self.type,
            "sub_type": self.sub_type,
            "properties": self.properties,
            "schema": self.schema,
        }

        if self.description is not None:
            return_dict["description"] = self.description

        return return_dict


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


class PropertyValue(TypedDict, total=True):
    """Artifacts for a property."""

    artifacts: TAnyPropertyTypedDict


PropertiesValue = typing.Dict[str, PropertyValue]


class _ModelTypedDictBase(TypedDict, total=False):
    """TypedDict representation of the model artifacts."""

    inherits: bool
    parent: str
    description: str
    mixins: TMixins
    kwargs: TKwargs
    composite_index: IndexList
    composite_unique: UniqueList


class ModelTypedDict(_ModelTypedDictBase, total=True):
    """TypedDict representation of the model artifacts."""

    tablename: str


class _ModelValueBase(TypedDict, total=False):
    """Record artifacts of a model."""

    properties: PropertiesValue


class ModelValue(_ModelValueBase, total=True):
    """Record artifacts of a model."""

    artifacts: ModelTypedDict


class ModelBackrefArtifacts(typing.NamedTuple):
    """Artifacts for model back references."""

    type: BackrefSubType
    child: str


@dataclasses.dataclass
class ModelExPropertiesArtifacts:
    """Information about a model excluding its properties."""

    tablename: str
    inherits: typing.Optional[bool]
    parent: typing.Optional[str]
    description: typing.Optional[str]
    mixins: typing.Optional[TMixins]
    kwargs: typing.Optional[TKwargs]
    composite_index: typing.Optional[IndexList]
    composite_unique: typing.Optional[UniqueList]
    backrefs: typing.List[typing.Tuple[str, ModelBackrefArtifacts]]

    def to_dict(self) -> ModelTypedDict:
        """Convert to dictionary."""
        return_dict: ModelTypedDict = {"tablename": self.tablename}

        opt_keys: typing.List[
            Literal[
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


@dataclasses.dataclass
class ModelArtifacts(ModelExPropertiesArtifacts):
    """Full information about a model."""

    properties: typing.List[typing.Tuple[str, TAnyPropertyArtifacts]]


ModelsValue = typing.Dict[str, ModelValue]


class SpecValue(TypedDict, total=False):
    """Record artifacts for a specification."""

    models: ModelsValue


ModelsModelArtifacts = typing.Dict[str, ModelArtifacts]
