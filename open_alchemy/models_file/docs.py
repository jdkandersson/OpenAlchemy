"""Functions for generating documentation for a model."""

import textwrap

from . import types

_DocstringWrapper = textwrap.TextWrapper(width=74)  # pylint: disable=invalid-name
_AttrWrapper = textwrap.TextWrapper(width=70)  # pylint: disable=invalid-name
_DEFAULT_DOCSTRING = "SQLAlchemy model protocol."


def docstring(artifacts: types.SQLAlchemyModelArtifacts) -> str:
    """
    Create docstring from description.

    Args:
        description: The description of the model.

    Returns:
        The docstring for the model.

    """
    if artifacts.description is None:
        return _DEFAULT_DOCSTRING

    wrapped_description = _DocstringWrapper.wrap(artifacts.description)
    joined_description = "\n    ".join(wrapped_description)
    return f"""
    {_DEFAULT_DOCSTRING}

    {joined_description}
    """


def attr(artifacts: types.ColumnArtifacts, model_name: str) -> str:
    """
    Calculate attribute documentation.

    Args:
        artifacts: The artifacts for the column to produce attribute documentation for.
        model_name: The name of the model that contains the attribute.

    Returns:
        The documentation for the attribute.

    """
    # Calculating docs for the attribute
    description: str
    if artifacts.description is not None:
        description = artifacts.description
    else:
        description = f"The {artifacts.name} of the {model_name}."
    doc = f"{artifacts.name}: {description}"

    # Wrapping and joining
    wrapped_doc = _AttrWrapper.wrap(doc)
    return "\n            ".join(wrapped_doc)
