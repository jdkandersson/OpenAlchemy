"""Generate models files based on individual models."""

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


def generate(*, models: typing.List[str]) -> str:
    """
    Generate the models file.

    Args:
        models: The models to add to the models file.

    Returns:
        The source for the models file.

    """
    imports: typing.Set[str] = set()
    for model in models:
        if "typing." in model:
            imports.add("typing")
        if "datetime." in model:
            imports.add("datetime")

    template = jinja2.Template(_TEMPLATE, trim_blocks=True)
    return template.render(imports=imports, models=models)
