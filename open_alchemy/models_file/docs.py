"""Functions for generating documentation for a model."""

import functools
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
    if artifacts.description is None and artifacts.empty:
        return _DEFAULT_DOCSTRING

    # Calculate description
    description: str
    if artifacts.description is None:
        description = f"""
    {_DEFAULT_DOCSTRING}"""
    else:
        wrapped_description = _DocstringWrapper.wrap(artifacts.description)
        joined_description = "\n    ".join(wrapped_description)
        description = f"""
    {_DEFAULT_DOCSTRING}

    {joined_description}"""

    # Calculate docs for the attributes
    attr_docs = ""
    if not artifacts.empty:
        attr_model_name_set = functools.partial(attr, model_name=artifacts.name)
        mapped_attrs = map(attr_model_name_set, artifacts.columns)
        joined_attrs = "\n        ".join(mapped_attrs)
        attr_docs = f"""

    Attrs:
        {joined_attrs}"""

    return f"""{description}{attr_docs}

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
