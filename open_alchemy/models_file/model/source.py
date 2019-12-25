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
# Overall template
_TEMPLATE_FILENAME = os.path.join(_DIRECTORY, "template.j2")
with open(_TEMPLATE_FILENAME) as in_file:
    _TEMPLATE = in_file.read()


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


def typed_dict_required(*, artifacts: types.TypedDictArtifacts) -> str:
    """
    Generate the TypedDict for required properties source code.

    Args:
        artifacts: The artifacts required for the TypedDict source code.

    Returns:
        The TypedDict for required properties source code.

    """
    template = jinja2.Template(_TYPED_DICT_REQUIRED_TEMPLATE)
    return template.render(artifacts=artifacts)


def typed_dict_not_required(*, artifacts: types.TypedDictArtifacts) -> str:
    """
    Generate the TypedDict for not required properties source code.

    Args:
        artifacts: The artifacts required for the TypedDict source code.

    Returns:
        The TypedDict for not required properties source code.

    """
    template = jinja2.Template(_TYPED_DICT_NOT_REQUIRED_TEMPLATE)
    return template.render(artifacts=artifacts)


def generate(*, artifacts: types.ModelArtifacts) -> str:
    """
    Generate the overall template with the TypedDict and SQLAlchemy model.

    Args:
        artifacts: The artifacts for the model.

    Returns:
        The source code for the template.

    """
    # Construct individual source code
    sqlalchemy_source = sqlalchemy(artifacts=artifacts.sqlalchemy)
    typed_dict_required_source = typed_dict_required(artifacts=artifacts.typed_dict)
    typed_dict_not_required_source = typed_dict_not_required(
        artifacts=artifacts.typed_dict
    )

    # Construct overall source code
    template = jinja2.Template(_TEMPLATE, trim_blocks=True)
    return template.render(
        artifacts=artifacts,
        typed_dict_required=typed_dict_required_source,
        typed_dict_not_required=typed_dict_not_required_source,
        sqlalchemy=sqlalchemy_source,
    )
