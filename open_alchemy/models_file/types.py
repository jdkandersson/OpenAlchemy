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

    name: str
    type: str


@dataclasses.dataclass
class ModelArtifacts:
    """Artifacts for a model template."""

    name: str
    columns: typing.List[ColumnArtifacts]
