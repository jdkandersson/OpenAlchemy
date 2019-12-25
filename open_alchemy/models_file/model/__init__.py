"""Generate a model class based on artifacts."""

import os
import typing

import jinja2

from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import types
from . import type_ as _type

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


def generate_source(*, artifacts: types.ModelArtifacts) -> str:
    """
    Generate python class for a model.

    Args:
        artifacts: The artifacts required to generate the class.

    Returns:
        The source code for the class of the model.

    """
    template = jinja2.Template(_TEMPLATE)
    return template.render(model=artifacts)


def generate(*, schema: oa_types.Schema, name: str) -> str:
    """
    Generate the class source from the schema.

    Args:
        schema: The schema of the model.
        name: The name of the model.

    Returns:
        The source code for the model class.

    """
    required = set(schema.get("required", []))

    columns: typing.List[types.ColumnArtifacts] = []
    for property_name, property_schema in schema["properties"].items():
        column_artifacts = gather_column_artifacts(
            schema=property_schema, required=property_name in required
        )

        column_type = _type.model(artifacts=column_artifacts)

        columns.append(types.ColumnArtifacts(type=column_type, name=property_name))

    artifacts = types.ModelArtifacts(name=name, columns=columns)
    return generate_source(artifacts=artifacts)
