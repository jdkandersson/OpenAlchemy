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

    arg_input_source = arg_input(artifacts=artifacts.arg)
    arg_kwargs_source = arg_kwargs(artifacts=artifacts.arg)

    return template.render(
        artifacts=artifacts,
        arg_input_source=arg_input_source,
        arg_kwargs_source=arg_kwargs_source,
    )


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


def _arg_input_single_arg_required(artifacts: types.ColumnArgArtifacts) -> str:
    """
    Transform the name and type of a single required argument to the input source.

    Args:
        artifacts: The artifacts for generating the argument for a column.

    Returns:
        The source for the argument for the column.

    """
    return f", {artifacts.name}: {artifacts.init_type}"


def _arg_input_single_arg_not_required(artifacts: types.ColumnArgArtifacts) -> str:
    """
    Transform the name and type of a single not required argument to the input source.

    Args:
        artifacts: The artifacts for generating the argument for a column.

    Returns:
        The source for the argument for the column.

    """
    required_source = _arg_input_single_arg_required(artifacts=artifacts)
    return f"{required_source} = None"


def arg_input(*, artifacts: types.ArgArtifacts) -> str:
    """
    Generate the arguments for the signature of __init__ and from_dict for a model.

    Args:
        artifacts: The artifacts for the arguments.

    Returns:
        The argument signature for the __init__ and from_dict functions.

    """
    required_sources = map(_arg_input_single_arg_required, artifacts.required)
    not_required_sources = map(
        _arg_input_single_arg_not_required, artifacts.not_required
    )
    return f'{"".join(required_sources)}{"".join(not_required_sources)}'


def _arg_kwargs_single_arg_required(artifacts: types.ColumnArgArtifacts) -> str:
    """
    Transform the name of a single required argument to the kwargs source.

    Args:
        artifacts: The artifacts for generating the kwarg for a column.

    Returns:
        The source for the kwargs for the column.

    """
    return f'"{artifacts.name}": {artifacts.name}'


def _arg_kwargs_single_arg_not_required(artifacts: types.ColumnArgArtifacts) -> str:
    """
    Transform the name of a single not required argument to the kwargs source.

    Args:
        artifacts: The artifacts for generating the kwarg for a column.

    Returns:
        The source for the kwargs for the column.

    """
    return f"""
        if {artifacts.name} is not None:
            kwargs["{artifacts.name}"] = {artifacts.name}"""


def arg_kwargs(*, artifacts: types.ArgArtifacts) -> str:
    """
    Generate the kwargs generation code for __init__ and from_dict for a model.

    Args:
        artifacts: The artifacts for the argument.

    Returns:
        The source code for generating the kwargs.

    """
    required_sources = map(_arg_kwargs_single_arg_required, artifacts.required)
    required_source = ", ".join(required_sources)
    not_required_sources = map(
        _arg_kwargs_single_arg_not_required, artifacts.not_required
    )
    not_required_source = "".join(not_required_sources)
    return f"""kwargs = {{{required_source}}}{not_required_source}"""


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
