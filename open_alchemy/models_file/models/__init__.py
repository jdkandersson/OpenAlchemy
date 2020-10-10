"""Generate models files based on individual models."""

import os
import sys
import typing

import jinja2

_DIRECTORY = os.path.dirname(__file__)
_TEMPLATE_FILE = os.path.join(_DIRECTORY, "template.j2")
with open(_TEMPLATE_FILE) as in_file:
    _TEMPLATE = in_file.read()

_ALL_IMPORTS = {"datetime", "typing"}


def generate(*, models: typing.List[str]) -> str:
    """
    Generate the models file.

    Args:
        models: The models to add to the models file.

    Returns:
        The source for the models file.

    """
    imports: typing.Set[str] = {"typing"}
    for model in models:
        if imports == _ALL_IMPORTS:
            break
        if "datetime." in model:
            imports.add("datetime")

    template = jinja2.Template(_TEMPLATE, trim_blocks=True)
    return template.render(
        imports=sorted(list(imports)),
        models=models,
        python_minor_version=sys.version_info[1],
    )
