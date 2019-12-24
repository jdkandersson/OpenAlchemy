"""Generate a model class based on artifacts."""

import os
import typing

import jinja2

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


# def _calculate_type(
#     *,
#     type str,
#     format_: typing.Optional[str],
#     nullable: typing.Optional[bool],
#     required: bool,
# ):
#     """
#     Calculate the python type of a column.
#     """


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
