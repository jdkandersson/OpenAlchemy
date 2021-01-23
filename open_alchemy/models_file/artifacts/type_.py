"""Functions for calculating the type."""

from open_alchemy import types
from open_alchemy.helpers import calculate_nullable
from open_alchemy.helpers import type_ as type_helper
from open_alchemy.schemas import artifacts as schemas_artifacts

_SIMPLE_TYPE_STRING_FORMAT_MAPPING = {
    "binary": "bytes",
    "date": "datetime.date",
    "date-time": "datetime.datetime",
}


_SIMPLE_TYPE_MAPPING = {
    "string": lambda format_: _SIMPLE_TYPE_STRING_FORMAT_MAPPING[format_]
    if format_ in _SIMPLE_TYPE_STRING_FORMAT_MAPPING
    else "str",
    "integer": lambda _: "int",
    "number": lambda _: "float",
    "boolean": lambda _: "bool",
}


def _model_simple_property(
    *, artifacts: schemas_artifacts.types.SimplePropertyArtifacts
) -> str:
    """Calculate the Python type of a simple property."""
    assert artifacts.open_api.type in type_helper.SIMPLE_TYPES
    type_ = _SIMPLE_TYPE_MAPPING[artifacts.open_api.type](artifacts.open_api.format)
    optional = calculate_nullable.calculate_nullable(
        nullable=artifacts.open_api.nullable,
        generated=artifacts.extension.autoincrement is True,
        required=artifacts.required,
        defaulted=artifacts.open_api.default is not None
        or artifacts.extension.server_default is not None,
    )

    if optional:
        return f"typing.Optional[{type_}]"
    return type_


_RELATIONSHIP_TYPE_MAPPING = {
    types.RelationshipType.MANY_TO_ONE: lambda parent: f'"T{parent}"',
    types.RelationshipType.ONE_TO_ONE: lambda parent: f'"T{parent}"',
    types.RelationshipType.ONE_TO_MANY: (
        lambda parent: f'typing.Sequence["T{parent}"]'
    ),
    types.RelationshipType.MANY_TO_MANY: (
        lambda parent: f'typing.Sequence["T{parent}"]'
    ),
}


def _model_relationship_property(
    *, artifacts: schemas_artifacts.types.TAnyRelationshipPropertyArtifacts
) -> str:
    """Calculate the Python type of a relationship property."""
    type_ = _RELATIONSHIP_TYPE_MAPPING[artifacts.sub_type](artifacts.parent)

    if (
        artifacts.sub_type == types.RelationshipType.ONE_TO_MANY
        or artifacts.sub_type == types.RelationshipType.MANY_TO_MANY
    ):
        return type_

    optional = calculate_nullable.calculate_nullable(
        nullable=artifacts.nullable,
        generated=False,
        required=artifacts.required,
        defaulted=False,
    )

    if optional:
        return f"typing.Optional[{type_}]"
    return type_


def model(*, artifacts: schemas_artifacts.types.TAnyPropertyArtifacts) -> str:
    """
    Calculate the Python type of a property.

    Assume that the property is not a back reference.

    Args:
        artifacts: The artifacts for the property.

    Returns:
        The equivalent Python type.

    """
    assert artifacts.type != types.PropertyType.BACKREF

    if artifacts.type == types.PropertyType.SIMPLE:
        return _model_simple_property(artifacts=artifacts)

    if artifacts.type == types.PropertyType.RELATIONSHIP:
        return _model_relationship_property(artifacts=artifacts)

    return "typing.Any"


def typed_dict(*, artifacts: schemas_artifacts.types.TAnyPropertyArtifacts) -> str:
    """
    Calculate the Python type of a column for a TypedDict.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the TypedDict.

    """
    model_type: str
    if artifacts.type != types.PropertyType.BACKREF:
        # Calculate type the same way as for the model
        model_type = model(artifacts=artifacts)
    else:
        inner_type = "typing.Dict[str, typing.Union[int, float, str, bool]]"
        if artifacts.sub_type == schemas_artifacts.types.BackrefSubType.OBJECT:
            model_type = f"typing.Optional[{inner_type}]"
        else:
            model_type = f"typing.Sequence[{inner_type}]"

    # No more checks if JSON
    if artifacts.type == types.PropertyType.JSON:
        return model_type

    # Modify the type in case of a relationship
    if artifacts.type == types.PropertyType.RELATIONSHIP:
        model_type = model_type.replace(
            f"T{artifacts.parent}", f"{artifacts.parent}Dict"
        )

    if artifacts.type == types.PropertyType.SIMPLE:
        # Revert back to str for binary, date and date-time
        if artifacts.open_api.format == "binary":
            model_type = model_type.replace("bytes", "str")
        if artifacts.open_api.format == "date":
            model_type = model_type.replace("datetime.date", "str")
        if artifacts.open_api.format == "date-time":
            model_type = model_type.replace("datetime.datetime", "str")

    return model_type


def arg_init(*, artifacts: schemas_artifacts.types.TAnyPropertyArtifacts) -> str:
    """
    Calculate the Python type of a column for the arguments of __init__.

    Assume that the property is not a back reference.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the argument for the column.

    """
    assert artifacts.type != types.PropertyType.BACKREF

    model_type = model(artifacts=artifacts)

    # If has a default value, remove optional
    if artifacts.type == types.PropertyType.SIMPLE:
        if artifacts.open_api.default is not None:
            if not model_type.startswith("typing.Optional["):
                return model_type
            return model_type[16:-1]

    # Add optional if not required unless already optional
    if not artifacts.required and not model_type.startswith("typing.Optional["):
        return f"typing.Optional[{model_type}]"
    return model_type


def arg_from_dict(*, artifacts: schemas_artifacts.types.TAnyPropertyArtifacts) -> str:
    """
    Calculate the Python type of a column for the arguments of from_dict.

    Assume that the property is not a back reference.

    Args:
        artifacts: The artifacts from the schema of the column.

    Returns:
        The equivalent Python type for the argument for the column.

    """
    assert artifacts.type != types.PropertyType.BACKREF

    # Calculate type the same way as for the model
    init_type = arg_init(artifacts=artifacts)

    # No more checks if JSON
    if artifacts.type == types.PropertyType.JSON:
        return init_type

    # Modify the type in case of relationship
    if artifacts.type == types.PropertyType.RELATIONSHIP:
        init_type = init_type.replace(f"T{artifacts.parent}", f"{artifacts.parent}Dict")

    return init_type
