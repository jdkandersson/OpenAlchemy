"""Functions for calculating the type."""

from open_alchemy import exceptions
from open_alchemy import helpers

from .. import types


def _string_mapping(artifacts: types.ColumnSchemaArtifacts) -> str:
    """Calculate type for string."""
    if artifacts.extension.json:
        return "str"
    if artifacts.open_api.format == "binary":
        return "bytes"
    if artifacts.open_api.format == "date":
        return "datetime.date"
    if artifacts.open_api.format == "date-time":
        return "datetime.datetime"
    return "str"


def _array_mapping(artifacts: types.ColumnSchemaArtifacts) -> str:
    """Calculate type for array."""
    if artifacts.extension.json:
        return "typing.Sequence"
    return f'typing.Sequence["T{artifacts.extension.de_ref}"]'


def _object_mapping(artifacts: types.ColumnSchemaArtifacts) -> str:
    """Calculate type for object."""
    if artifacts.extension.json:
        return "typing.Dict"
    return f'"T{artifacts.extension.de_ref}"'


_TYPE_MAPPING = {
    "string": _string_mapping,
    "integer": lambda _: "int",
    "number": lambda _: "float",
    "boolean": lambda _: "bool",
    "array": _array_mapping,
    "object": _object_mapping,
}


def model(*, artifacts: types.ColumnSchemaArtifacts) -> str:
    """
    Calculate the Python type of a column.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type.

    """
    # Determine underlying type
    return_type = _TYPE_MAPPING[artifacts.open_api.type](artifacts)
    if artifacts.open_api.type == "array" and not artifacts.extension.json:
        return return_type

    # Determine whether the type is optional
    optional = helpers.calculate_nullable(
        nullable=artifacts.open_api.nullable,
        generated=artifacts.extension.generated is True,
        required=artifacts.open_api.required,
        defaulted=artifacts.open_api.default is not None,
    )
    if optional:
        return f"typing.Optional[{return_type}]"
    return return_type


def typed_dict(*, artifacts: types.ColumnSchemaArtifacts) -> str:
    """
    Calculate the Python type of a column for a TypedDict.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the TypedDict.

    """
    # Calculate type the same way as for the model
    model_type = model(artifacts=artifacts)

    # No more checks if JSON
    if artifacts.extension.json:
        return model_type

    # Modify the type in case of object or array
    if artifacts.open_api.type in {"object", "array"}:
        if artifacts.extension.de_ref is None:
            raise exceptions.MissingArgumentError(
                "The schema for the property of an object reference must include "
                "x-de-$ref with the name of the model being referenced."
            )
        model_type = model_type.replace(
            f"T{artifacts.extension.de_ref}", f"{artifacts.extension.de_ref}Dict"
        )
    # Revert back to str for binary, date and date-time
    if artifacts.open_api.format == "binary":
        model_type = model_type.replace("bytes", "str")
    if artifacts.open_api.format == "date":
        model_type = model_type.replace("datetime.date", "str")
    if artifacts.open_api.format == "date-time":
        model_type = model_type.replace("datetime.datetime", "str")

    return model_type


def arg_init(*, artifacts: types.ColumnSchemaArtifacts) -> str:
    """
    Calculate the Python type of a column for the arguments of __init__.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the argument for the column.

    """
    model_type = model(artifacts=artifacts)

    # If has a default value, remove optional
    if artifacts.open_api.default is not None:
        if not model_type.startswith("typing.Optional["):
            return model_type
        return model_type[16:-1]

    # Add optional if not required unless already optional
    if not artifacts.open_api.required and not model_type.startswith(
        "typing.Optional["
    ):
        return f"typing.Optional[{model_type}]"
    return model_type


def arg_from_dict(*, artifacts: types.ColumnSchemaArtifacts) -> str:
    """
    Calculate the Python type of a column for the arguments of from_dict.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the argument for the column.

    """
    # Calculate type the same way as for the model
    init_type = arg_init(artifacts=artifacts)

    # No more checks if JSON
    if artifacts.extension.json:
        return init_type

    # Modify the type in case of object or array
    if artifacts.open_api.type in {"object", "array"}:
        if artifacts.extension.de_ref is None:
            raise exceptions.MissingArgumentError(
                "The schema for the property of an object reference must include "
                "x-de-$ref with the name of the model being referenced."
            )
        init_type = init_type.replace(
            f"T{artifacts.extension.de_ref}", f"{artifacts.extension.de_ref}Dict"
        )

    return init_type
