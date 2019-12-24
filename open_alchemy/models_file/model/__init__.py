"""Generate a model class based on artifacts."""

import os
import typing

import jinja2

from open_alchemy import helpers

from .. import types

# from open_alchemy import types as oa_types


_DIRECTORY = os.path.dirname(__file__)
_TEMPLATE_FILE = os.path.join(_DIRECTORY, "template.j2")
with open(_TEMPLATE_FILE) as in_file:
    _TEMPLATE = in_file.read()


# def gather_artifacts(*, schema: oa_types.Schema) -> types.ModelArtifacts:
#     """
#     Gather artifacts for generating the class of a models.

#     Assume the schema does not contain any $ref and allOf.
#     Assume that the schema is an object with at least 1 property.
#     Assume that each property has a type.

#     Args:
#         schema: The schema of the model.

#     Returns:
#         The artifacts for generating the class of a model.

#     """


def _calculate_type(
    *,
    type_: str,
    format_: typing.Optional[str],
    nullable: typing.Optional[bool],
    required: typing.Optional[bool],
):
    """
    Calculate the python type of a column.

    Args:
        type_: The OpenAPI type.
        format_: The OpenAPI format.
        nullable: Whether the property is nullable.
        required: Whether the property is required.

    Returns:
        The equivalent Python type.

    """
    # Determine underlying type
    return_type = "str"
    if type_ == "integer":
        return_type = "int"
    if type_ == "number":
        return_type = "float"
    if type_ == "boolean":
        return_type = "bool"
    if format_ == "binary":
        return_type = "bytes"
    if format_ == "date":
        return_type = "datetime.date"
    if format_ == "date-time":
        return_type = "datetime.datetime"

    # Determine whether the type is optional
    optional = helpers.calculate_nullable(nullable=nullable, required=required)
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
