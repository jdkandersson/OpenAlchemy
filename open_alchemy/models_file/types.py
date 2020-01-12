"""Types for model generation."""

import dataclasses
import typing


@dataclasses.dataclass
class ColumnSchemaArtifacts:
    """Artifacts from the OpenAPI schema."""

    # The type of the column
    type: str
    # The format of the column
    format: typing.Optional[str] = None
    # Whether the column is nullable
    nullable: typing.Optional[bool] = None
    # Whether the column is required
    required: typing.Optional[bool] = None
    # The model being reference for an object/array type
    de_ref: typing.Optional[str] = None
    # Whether the value of the column is generated (eg. through auto increment)
    generated: typing.Optional[bool] = None


@dataclasses.dataclass
class ColumnArtifacts:
    """Artifacts for the column portion of a model template."""

    # The name of the column
    name: str
    # The type of the column
    type: str


@dataclasses.dataclass
class ColumnArgArtifacts:
    """Artifacts for the __init__ and from_dict signatures of a model template."""

    # The name of the argument
    name: str
    # The type of the argument for __init__
    init_type: str
    # The type of the argument for from_dict
    from_dict_type: str


@dataclasses.dataclass
class ArgArtifacts:
    """Artifacts for the __init__ and from_dict args for a model."""

    # The artifacts for the arguments that are required
    required: typing.List[ColumnArgArtifacts]
    # The artifacts for the arguments that are not required
    not_required: typing.List[ColumnArgArtifacts]


@dataclasses.dataclass
class SQLAlchemyModelArtifacts:
    """Artifacts for the SQLAlchemy model."""

    # The name of the model
    name: str
    # Whether the columns are empty
    empty: bool
    # The columns for the model
    columns: typing.List[ColumnArtifacts]
    # The artifacts for the arguments for __init__ and from_dict
    arg: ArgArtifacts
    # The parent class
    parent_cls: str


@dataclasses.dataclass
class TypedDictClassArtifacts:
    """Artifacts for a TypedDict class."""

    # The properties for the TypedDict
    props: typing.List[ColumnArtifacts]
    # Whether the properties list is empty
    empty: bool
    # The name of the TypedDict
    name: typing.Optional[str]
    # The name of the parent class
    parent_class: typing.Optional[str]


@dataclasses.dataclass
class TypedDictArtifacts:
    """Artifacts for the TypedDicts for a model."""

    # The artifacts for the required TypedDict
    required: TypedDictClassArtifacts
    # The artifacts for the required TypedDict
    not_required: TypedDictClassArtifacts


@dataclasses.dataclass
class ModelArtifacts:
    """Artifacts for a model template."""

    # The artifacts for the SQLAlchemy model
    sqlalchemy: SQLAlchemyModelArtifacts
    # The artifacts for the TypedDicts
    typed_dict: TypedDictArtifacts
