"""Functions for handling foreign keys."""

import typing

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def check_required(
    *,
    artifacts: types.ColumnArtifacts,
    fk_logical_name: str,
    model_schema: types.Schema,
    schemas: types.Schemas,
) -> bool:
    """
    Check whether a foreign key has already been defined.

    Assume model_schema has already resolved any $ref and allOf at the object level.
    They may not have been resolved at the property level.

    Check whether the proposed logical name is already defined on the model schema. If
    it has been, check that the type is correct and that the foreign key reference has
    been defined and points to the correct column.

    Raise MalformedRelationshipError if a property has already been defined with the
    same name as is proposed for the foreign key but it has the wrong type or does not
    define the correct foreign key constraint.

    Args:
        artifacts: The artifacts of the foreign key.
        fk_logical_name: The proposed name for the foreign key property.
        model_schema: The schema for the model on which the foreign key is proposed to
            be added.
        schemas: Used to resolve any $ref at the property level.

    Returns:
        Whether defining the foreign key is necessary given the model schema.

    """
    properties = model_schema["properties"]
    model_fk_schema = properties.get(fk_logical_name)
    if model_fk_schema is None:
        return True
    model_fk_schema = helpers.schema.prepare(schema=model_fk_schema, schemas=schemas)

    # Check type
    model_fk_type = model_fk_schema.get("type")
    if model_fk_type is None:
        raise exceptions.MalformedRelationshipError(
            f"{fk_logical_name} does not have a type. "
        )
    if model_fk_type != artifacts.open_api.type:
        raise exceptions.MalformedRelationshipError(
            "The foreign key required for the relationship has a different type than "
            "the property already defined under that name. "
            f"The required type is {artifacts.open_api.type}. "
            f"The {fk_logical_name} property has the {model_fk_type} type."
        )

    # Check foreign key constraint
    model_foreign_key = helpers.ext_prop.get(
        source=model_fk_schema, name="x-foreign-key"
    )
    if model_foreign_key is None:
        raise exceptions.MalformedRelationshipError(
            f"The property already defined under {fk_logical_name} does not define a "
            'foreign key constraint. Use the "x-foreign-key" extension property to '
            "define a foreign key constraint, for example: "
            f'{artifacts.extension.foreign_key}".'
        )
    foreign_key = artifacts.extension.foreign_key
    # Should not happen
    if foreign_key is None:
        raise exceptions.MalformedRelationshipError(
            "Artifacts for constructing a foreign key does not include a foreign key "
            "constraint."
        )
    if model_foreign_key != artifacts.extension.foreign_key:
        raise exceptions.MalformedRelationshipError(
            "The foreign key required for the relationship has a different foreign "
            "key constraint than the property already defined under that name. "
            f"The required constraint is {artifacts.extension.foreign_key}. "
            f"The {fk_logical_name} property has the {model_foreign_key} constraint."
        )

    return False


def gather_artifacts(
    *,
    model_schema: types.Schema,
    logical_name: str,
    schemas: types.Schemas,
    fk_column: str,
    required: typing.Optional[bool] = None,
    nullable: typing.Optional[bool] = None,
) -> typing.Tuple[str, types.ColumnArtifacts]:
    """
    Gather artifacts for a foreign key to implement an object reference.

    Assume any object schema level allOf and $ref have already been resolved.

    Raise MalformedSchemaError if x-tablename or properties are missing. Also raise if
    the foreign key column is not found in the model schema or it does not have a type.

    Args:
        model_schema: The schema of the referenced model.
        logical_name: The logical name of the property with the object reference.
        schemas: All model schemas used to resolve any $ref.
        fk_column: The name of the foreign key column.
        required: Whether the foreign key is constructed for a property that is
            required.
        nullable: Whether the foreign key is constructed for a property that is
            nullable.

    Returns:
        The logical name of the foreign key and the artifacts required to construct it.

    """
    tablename = helpers.ext_prop.get(source=model_schema, name="x-tablename")
    if not tablename:
        raise exceptions.MalformedSchemaError(
            "Referenced object is missing x-tablename property."
        )
    properties = model_schema.get("properties")
    if properties is None:
        raise exceptions.MalformedSchemaError(
            "Referenced object does not have any properties."
        )
    fk_schema = properties.get(fk_column)
    if fk_schema is None:
        raise exceptions.MalformedSchemaError(
            f"Referenced object does not have {fk_column} property."
        )

    # Gather artifacts
    try:
        fk_type = helpers.peek.type_(schema=fk_schema, schemas=schemas)
    except exceptions.TypeMissingError:
        raise exceptions.MalformedSchemaError(
            f"Referenced object {fk_column} property does not have a type."
        )
    fk_format = helpers.peek.format_(schema=fk_schema, schemas=schemas)
    fk_max_length = helpers.peek.max_length(schema=fk_schema, schemas=schemas)
    fk_default = helpers.peek.default(schema=fk_schema, schemas=schemas)
    nullable = helpers.calculate_nullable(
        nullable=nullable,
        generated=False,
        required=required,
        defaulted=fk_default is not None,
    )

    # Construct return values
    return_logical_name = f"{logical_name}_{fk_column}"
    artifacts = types.ColumnArtifacts(
        open_api=types.OpenAPiColumnArtifacts(
            type=fk_type,
            format=fk_format,
            nullable=nullable,
            max_length=fk_max_length,
            default=fk_default,
        ),
        extension=types.ExtensionColumnArtifacts(
            foreign_key=f"{tablename}.{fk_column}"
        ),
    )
    return return_logical_name, artifacts


def gather_artifacts_helper(
    obj_artifacts: types.ObjectArtifacts,
    schemas: types.Schemas,
    required: typing.Optional[bool],
):
    """
    Gather foreign key artifacts based on object reference artifacts.

    Intended for use for the object reference handler.

    Args:
        obj_artifacts: The artifacts for the object reference.
        schemas: All model schemas used to resolve any $ref.
        required: Whether the foreign key is constructed for a property that is
            required.

    Returns:
        The artifacts for the foreign key.

    """
    return gather_artifacts(
        model_schema=obj_artifacts.spec,
        logical_name=obj_artifacts.logical_name,
        schemas=schemas,
        fk_column=obj_artifacts.fk_column,
        required=required,
        nullable=obj_artifacts.nullable,
    )
