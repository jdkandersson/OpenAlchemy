"""Validate the specification."""

import typing

from . import schemas_validation
from . import types


def check(*, spec: typing.Any) -> types.Result:
    """
    Check whether a specification is valid.

    The algorithm is:
    1. check that it is a dictionary,
    2. check that components is defined and that it is a dictionary and
    3. check that schemas is defined and that it is valid.

    Args:
        spec: The specification to check.

    Returns:
        Whether the specification is valid.

    """
    if not isinstance(spec, dict):
        return types.Result(False, "specification must be a dictionary")

    # Check components
    components = spec.get("components")
    if components is None:
        return types.Result(False, "specification must define components")
    if not isinstance(components, dict):
        return types.Result(False, "components value must be a dictionary")

    # Check schemas
    schemas = components.get("schemas")
    if schemas is None:
        return types.Result(False, "specification must define schemas")
    return schemas_validation.check(schemas=schemas)
