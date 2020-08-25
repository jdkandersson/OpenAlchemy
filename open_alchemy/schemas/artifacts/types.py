"""The artifact types."""

import dataclasses
import typing

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
