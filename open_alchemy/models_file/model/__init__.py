"""Generate a model class based on artifacts."""

import os
import typing

import jinja2

from open_alchemy import helpers
from open_alchemy import types as oa_types

from .. import types
from . import artifacts as _artifacts
from . import type_ as _type

_DIRECTORY = os.path.dirname(__file__)
_TEMPLATE_FILE = os.path.join(_DIRECTORY, "template.j2")
with open(_TEMPLATE_FILE) as in_file:
    _TEMPLATE = in_file.read()


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
    artifacts = _artifacts.calculate(schema=schema, name=name)
    return generate_source(artifacts=artifacts)
