"""Functions for generating documentation for a model."""

import textwrap
import typing

_DocstringWrapper = textwrap.TextWrapper(width=74)  # pylint: disable=invalid-name
_DEFAULT_DOCSTRING = "SQLAlchemy model protocol."


def docstring(description: typing.Optional[str]) -> str:
    """
    Create docstring from description.

    Args:
        description: The description of the model.

    Returns:
        The docstring for the model.

    """
    if description is None:
        return _DEFAULT_DOCSTRING

    wrapped_description = _DocstringWrapper.wrap(description)
    joined_description = "\n    ".join(wrapped_description)
    return f"""
    {_DEFAULT_DOCSTRING}

    {joined_description}
    """
