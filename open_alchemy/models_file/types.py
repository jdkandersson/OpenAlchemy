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
    # The columns for the model
    columns: typing.List[ColumnArtifacts]


@dataclasses.dataclass
class TypedDictArtifacts:
    """Artifacts for the TypedDicts for a model."""

    # The properties that are required
    required_props: typing.List[ColumnArtifacts]
    # The properties that are not required
    not_required_props: typing.List[ColumnArtifacts]
    # Whether the required list is empty
    required_empty: bool
    # Whether the not required list is empty
    not_required_empty: bool
    # The name of the TypedDict for properties that are required
    required_name: typing.Optional[str]
    # The name of the TypedDict for properties that are not required
    not_required_name: typing.Optional[str]


@dataclasses.dataclass
class ModelArtifacts:
    """Artifacts for a model template."""

    # The artifacts for the SQLAlchemy model
    sqlalchemy: SQLAlchemyModelArtifacts
    # The artifacts for the TypedDicts
    typed_dict: TypedDictArtifacts
