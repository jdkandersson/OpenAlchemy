"""Generate source code for a model."""

import os

import jinja2

from .. import types

_DIRECTORY = os.path.dirname(__file__)
# SQLAlchemy template
_SQLALCHEMY_TEMPLATE_FILENAME = os.path.join(_DIRECTORY, "sqlalchemy.j2")
with open(_SQLALCHEMY_TEMPLATE_FILENAME) as in_file:
    _SQLALCHEMY_TEMPLATE = in_file.read()
# TypedDict required template
_TYPED_DICT_REQUIRED_TEMPLATE_FILENAME = os.path.join(
    _DIRECTORY, "typed_dict_required.j2"
)
with open(_TYPED_DICT_REQUIRED_TEMPLATE_FILENAME) as in_file:
    _TYPED_DICT_REQUIRED_TEMPLATE = in_file.read()
# TypedDict not required template
_TYPED_DICT_NOT_REQUIRED_TEMPLATE_FILENAME = os.path.join(
    _DIRECTORY, "typed_dict_not_required.j2"
)
with open(_TYPED_DICT_NOT_REQUIRED_TEMPLATE_FILENAME) as in_file:
    _TYPED_DICT_NOT_REQUIRED_TEMPLATE = in_file.read()


def sqlalchemy(*, artifacts: types.SQLAlchemyModelArtifacts) -> str:
    """
    Generate the SQLAlchemy model source code.

    Args:
        artifacts: The artifacts required for the SQLAlchemy model source code.

    Returns:
        The SQLAlchemy model source code.

    """
    template = jinja2.Template(_SQLALCHEMY_TEMPLATE)
    return template.render(artifacts=artifacts)
