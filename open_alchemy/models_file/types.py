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
class ModelArtifacts:
    """Artifacts for a model template."""

    # The name of the model
    name: str
    # The columns for the model
    columns: typing.List[ColumnArtifacts]

    # The properties that are required for the TypedDict for the model
    td_required_props: typing.List[ColumnArtifacts] = dataclasses.field(
        default_factory=list
    )
    # The properties that are not required for the TypedDict for the model
    td_not_required_props: typing.List[ColumnArtifacts] = dataclasses.field(
        default_factory=list
    )
    # Whether the required list is empty
    td_required_empty: bool = False
    # Whether the not required list is empty
    td_not_required_empty: bool = False
    # The name of the TypedDict for required properties
    td_required_name: typing.Optional[str] = None
    # The name of the TypedDict for properties that are not required
    td_not_required_name: typing.Optional[str] = None
