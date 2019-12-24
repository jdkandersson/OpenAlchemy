"""Generate a model class based on artifacts."""

import os
import typing

import jinja2

from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import types

_DIRECTORY = os.path.dirname(__file__)
_TEMPLATE_FILE = os.path.join(_DIRECTORY, "template.j2")
with open(_TEMPLATE_FILE) as in_file:
    _TEMPLATE = in_file.read()


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


def _calculate_type(*, artifacts: types.ColumnSchemaArtifacts):
    """
    Calculate the python type of a column.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type.

    """
    # Determine underlying type
    return_type = "str"
    if artifacts.type == "integer":
        return_type = "int"
    if artifacts.type == "number":
        return_type = "float"
    if artifacts.type == "boolean":
        return_type = "bool"
    if artifacts.type == "object":
        assert artifacts.de_ref is not None
        return_type = artifacts.de_ref
    if artifacts.type == "array":
        assert artifacts.de_ref is not None
        return_type = f"typing.Sequence[{artifacts.de_ref}]"
    if artifacts.format == "binary":
        return_type = "bytes"
    if artifacts.format == "date":
        return_type = "datetime.date"
    if artifacts.format == "date-time":
        return_type = "datetime.datetime"

    # Determine whether the type is optional
    optional = helpers.calculate_nullable(
        nullable=artifacts.nullable, required=artifacts.required
    )
    if optional:
        return f"typing.Optional[{return_type}]"
    return return_type


def generate(*, artifacts: types.ModelArtifacts) -> str:
    """
    Generate python class for a model.

    Args:
        artifacts: The artifacts required to generate the class.

    Returns:
        The source code for the class of the model.

    """
    template = jinja2.Template(_TEMPLATE)
    return template.render(model=artifacts)
