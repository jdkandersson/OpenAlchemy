"""Generate a model class based on artifacts."""

import os

import jinja2

from .. import types

_DIRECTORY = os.path.dirname(__file__)
_TEMPLATE_FILE = os.path.join(_DIRECTORY, "template.j2")
with open(_TEMPLATE_FILE) as in_file:
    _TEMPLATE = in_file.read()


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
