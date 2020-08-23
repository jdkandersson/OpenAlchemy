"""Retrieve mixin classes."""

import importlib
import inspect
import typing

from . import exceptions


def _import_mixin(mixin: str) -> typing.Type:
    """Import the mixin."""
    assert "." in mixin
    module_name, class_name = mixin.rsplit(".", 1)

    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise exceptions.MalformedExtensionPropertyError(
            f'error when attempting to import "{module_name}"'
        ) from exc

    try:
        class_ = getattr(module, class_name)
    except AttributeError as exc:
        raise exceptions.MalformedExtensionPropertyError(
            f'the module "{module_name}" does not have the "{class_name}" class'
        ) from exc

    if not inspect.isclass(class_):
        raise exceptions.MalformedExtensionPropertyError(
            f'"{class_name}" is not a class'
        )

    return class_


def get(*, mixins: typing.List[str]) -> typing.Tuple[typing.Type, ...]:
    """
    Import the mixins.

    Assume that the mixins are valid instances of x-mixins.

    Raise MalformedExtensionPropertyError if the value of x-mixins cannot be imported
    or is not a class.

    Algorithm:
    1. split each mixin on the last dot,
    2. use the first part to import the module,
    3. use the second part to retrieve the class and
    4. check that the class is actually a class.

    Args:
        mixins: The mixins to load.

    Returns:
        The mixin classes.

    """
    return tuple(map(_import_mixin, mixins))
