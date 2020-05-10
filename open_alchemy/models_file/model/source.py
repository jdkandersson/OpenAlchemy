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

    arg_init_source = arg_init(artifacts=artifacts.arg)
    arg_from_dict_source = arg_from_dict(artifacts=artifacts.arg)

    return template.render(
        artifacts=artifacts,
        arg_init_source=arg_init_source,
        arg_from_dict_source=arg_from_dict_source,
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


def _arg_single_required(artifacts: types.ColumnArgArtifacts, name: str) -> str:
    """
    Transform the name and type of a single required argument to the input source.

    Args:
        artifacts: The artifacts for generating the argument for a column.
        name: The attribute name to use for the type.

    Returns:
        The source for the argument for the column.

    """
    return f", {artifacts.name}: {getattr(artifacts, name)}"


def _arg_single_not_required(artifacts: types.ColumnArgArtifacts, name: str) -> str:
    """
    Transform the name and type of a single not required argument to the input source.

    Args:
        artifacts: The artifacts for generating the argument for a column.
        name: The attribute name to use for the type.

    Returns:
        The source for the argument for the column.

    """
    required_source = _arg_single_required(artifacts, name)
    return f"{required_source} = {artifacts.default}"


def _arg(*, artifacts: types.ArgArtifacts, name: str) -> str:
    """
    Generate the arguments for a function signature of a model.

    Args:
        artifacts: The artifacts for the arguments.
        name: The attribute name to use for the type.

    Returns:
        The argument signature for the functions.

    """
    required_sources = map(
        lambda artifacts: _arg_single_required(artifacts, name), artifacts.required
    )
    not_required_sources = map(
        lambda artifacts: _arg_single_not_required(artifacts, name),
        artifacts.not_required,
    )
    return f'{"".join(required_sources)}{"".join(not_required_sources)}'


def arg_init(*, artifacts: types.ArgArtifacts) -> str:
    """
    Generate the arguments for the signature of __init__ for a model.

    Args:
        artifacts: The artifacts for the arguments.

    Returns:
        The argument signature for the __init__ functions.

    """
    return _arg(artifacts=artifacts, name="init_type")


def _check_not_read_only_arg(arg: types.ColumnArgArtifacts) -> bool:
    """Check whether an argument is not read only."""
    return arg.read_only is not True


def remove_read_only_args(*, artifacts: types.ArgArtifacts) -> types.ArgArtifacts:
    """
    Remove read only arguments from the artifacts.

    Args:
        artifacts: The artifacts to filter.

    Returns:
        The filtered artifacts.

    """
    return types.ArgArtifacts(
        required=list(filter(_check_not_read_only_arg, artifacts.required)),
        not_required=list(filter(_check_not_read_only_arg, artifacts.not_required)),
    )


def arg_from_dict(*, artifacts: types.ArgArtifacts) -> str:
    """
    Generate the arguments for the signature of from_dict for a model.

    Args:
        artifacts: The artifacts for the arguments.

    Returns:
        The argument signature for the from_dict functions.

    """
    no_read_only_artifacts = remove_read_only_args(artifacts=artifacts)
    return _arg(artifacts=no_read_only_artifacts, name="from_dict_type")


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
