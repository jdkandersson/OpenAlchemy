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


@dataclasses.dataclass
class ColumnArtifacts:
    """Artifacts for the column portion of a model template."""

    # The name of the column
    name: str
    # The type of the column
    type: str


@dataclasses.dataclass
class SQLAlchemyModelArtifacts:
    """Artifacts for the SQLAlchemy model."""

    # The name of the model
    name: str
    # Whether the columns are empty
    empty: bool
    # The columns for the model
    columns: typing.List[ColumnArtifacts]


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
