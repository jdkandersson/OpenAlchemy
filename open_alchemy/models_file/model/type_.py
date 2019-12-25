"""Functions for calculating the type."""

from open_alchemy import helpers

from .. import types


def model(*, artifacts: types.ColumnSchemaArtifacts):
    """
    Calculate the Python type of a column.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type.

    """
    # Determine underlying type
    return_type = "str"
    if artifacts.type == "integer":
        return_type = "int"
    if artifacts.type == "number":
        return_type = "float"
    if artifacts.type == "boolean":
        return_type = "bool"
    if artifacts.type == "object":
        return_type = f'"{artifacts.de_ref}"'
    if artifacts.type == "array":
        return f'typing.Sequence["{artifacts.de_ref}"]'
    if artifacts.format == "binary":
        return_type = "bytes"
    if artifacts.format == "date":
        return_type = "datetime.date"
    if artifacts.format == "date-time":
        return_type = "datetime.datetime"

    # Determine whether the type is optional
    optional = helpers.calculate_nullable(
        nullable=artifacts.nullable, required=artifacts.required
    )
    if optional:
        return f"typing.Optional[{return_type}]"
    return return_type


def typed_dict(*, artifacts: types.ColumnSchemaArtifacts):
    """
    Calculate the Python type of a column for a TypedDict.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the TypedDict.

    """
    # Calculate type the same way as for the model
    model_type = model(artifacts=artifacts)

    # Modify the type in case of object or array
    if artifacts.type in {"object", "array"}:
        model_type = model_type.replace(artifacts.de_ref, f"{artifacts.de_ref}Dict")

    return model_type
