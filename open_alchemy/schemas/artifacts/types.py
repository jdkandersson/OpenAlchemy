"""The artifact types."""

import dataclasses
import typing

from ... import types
from .. import helpers


@dataclasses.dataclass
class PropertyArtifacts:
    """Information about a property."""

    property_type: typing.Literal[
        helpers.property_.type_.Type.SIMPLE,
        helpers.property_.type_.Type.JSON,
        helpers.property_.type_.Type.RELATIONSHIP,
        helpers.property_.type_.Type.BACKREF,
    ]


@dataclasses.dataclass
class SimplePropertyArtifacts(PropertyArtifacts):
    """Information about a simple property."""

    property_type: typing.Literal[helpers.property_.type_.Type.SIMPLE]

    type_: str
    format_: typing.Optional[str]


TMixins = typing.List[str]
TKwargs = typing.Dict[str, typing.Any]


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
