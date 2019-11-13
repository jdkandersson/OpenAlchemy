"""Check whether a property is readOnly."""

from open_alchemy import exceptions
from open_alchemy import types

from .get_ext_prop import get_ext_prop


def check_read_only(*, spec: types.Schema) -> bool:
    """
    Check whether the specification is a valid read only.

    Assume allOf and $ref have been resolved.

    Raise MalformedSchemaError if the type is an object or array or not defined.
    Raise MalformedSchemaError if the x-backref-column is not defined.

    Args:
        spec: The spec to check.

    Returns:
        Whether the property is a read only property.

    """
    # Check for readOnly
    read_only = spec.get("readOnly")
    if read_only is None or read_only is False:
        return False

    # Check type
    type_ = spec.get("type")
    if type_ is None:
        raise exceptions.MalformedSchemaError(
            "Every readOnly property must have a type."
        )
    if type_ == "object":
        raise exceptions.MalformedSchemaError(
            "readOnly properties cannot be an object."
        )
    if type_ == "array":
        items = spec.get("items")
        if items is None:
            raise exceptions.MalformedSchemaError(
                "A readOnly array must define its items."
            )
        items_type = items.get("type")
        if items_type is None:
            raise exceptions.MalformedSchemaError(
                "A readOnly array must define the type of its items."
            )
        if items_type in {"object", "array"}:
            raise exceptions.MalformedSchemaError(
                "A readOnly array must not have object or array item types."
            )

    # Check x-backref-column
    backref_column = get_ext_prop(source=spec, name="x-backref-column")
    if backref_column is None:
        raise exceptions.MalformedSchemaError(
            "Every readOnly property must define the column of the relationship to "
            'return using "x-backref-column".'
        )

    return True
