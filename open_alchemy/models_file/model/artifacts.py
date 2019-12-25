"""Functions for model artifacts."""

import typing

from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import types
from . import type_ as _type


def gather_column_artifacts(
    *, schema: oa_types.Schema, required: typing.Optional[bool]
) -> types.ColumnSchemaArtifacts:
    """
    Gather artifacts for generating the class of a models.

    Assume the schema does not contain any $ref and allOf.
    Assume that the schema is an object with at least 1 property.
    Assume that each property has a type.

    Args:
        schema: The schema of the model.

    Returns:
        The artifacts for generating the class of a model.

    """
    type_ = schema["type"]
    format_ = schema.get("format")
    nullable = schema.get("nullable")
    de_ref = None
    if type_ == "object":
        de_ref = helpers.get_ext_prop(source=schema, name="x-de-$ref")
    if type_ == "array":
        de_ref = helpers.get_ext_prop(source=schema["items"], name="x-de-$ref")

    return types.ColumnSchemaArtifacts(
        type=type_, format=format_, nullable=nullable, required=required, de_ref=de_ref
    )


def calculate(*, schema: oa_types.Schema, name: str) -> types.ModelArtifacts:
    """
    Calculate the model artifacts from the schema.

    Args:
        schema: The schema of the model
        name: The name of the model.

    Returns:
        The artifacts for the model.

    """
    required = set(schema.get("required", []))

    # Initialize lists
    columns: typing.List[types.ColumnArtifacts] = []
    td_required_props: typing.List[types.ColumnArtifacts] = []
    td_not_required_props: typing.List[types.ColumnArtifacts] = []

    # Calculate artifacts for properties
    for property_name, property_schema in schema["properties"].items():
        # Gather artifacts
        property_required = property_name in required
        column_artifacts = gather_column_artifacts(
            schema=property_schema, required=property_required
        )

        # Calculate the type
        column_type = _type.model(artifacts=column_artifacts)
        td_prop_type = _type.typed_dict(artifacts=column_artifacts)

        # Add artifacts to the lists
        columns.append(types.ColumnArtifacts(type=column_type, name=property_name))
        prop_artifacts = types.ColumnArtifacts(type=td_prop_type, name=property_name)
        if property_required:
            td_required_props.append(prop_artifacts)
        else:
            td_not_required_props.append(prop_artifacts)

    return types.ModelArtifacts(
        name=name,
        columns=columns,
        td_required_props=td_required_props,
        td_not_required_props=td_not_required_props,
    )
