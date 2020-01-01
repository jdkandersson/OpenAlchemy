"""Functions for handling foreign keys."""

from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types


def check_required(
    *,
    fk_spec: types.Schema,
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
        fk_spec: The proposed foreign key specification.
        fk_logical_name: The proposed name for the foreign key property.
        model_schema: The schema for the model on which the foreign key is proposed to
            be added.
        schemas: Used to resolve any $ref at the property level.

    Returns:
        Whether defining the foreign key is necessary given the model schema.

    """
    properties = model_schema["properties"]
    model_fk_spec = properties.get(fk_logical_name)
    if model_fk_spec is None:
        return True
    model_fk_spec = helpers.prepare_schema(schema=model_fk_spec, schemas=schemas)

    # Check type
    model_fk_type = model_fk_spec.get("type")
    if model_fk_type is None:
        raise exceptions.MalformedRelationshipError(
            f"{fk_logical_name} does not have a type. "
        )
    fk_type = fk_spec["type"]
    if model_fk_type != fk_type:
        raise exceptions.MalformedRelationshipError(
            "The foreign key required for the relationship has a different type than "
            "the property already defined under that name. "
            f"The required type is {fk_type}. "
            f"The {fk_logical_name} property has the {model_fk_type} type."
        )

    # Check foreign key constraint
    model_foreign_key = helpers.get_ext_prop(source=model_fk_spec, name="x-foreign-key")
    foreign_key = fk_spec["x-foreign-key"]
    if model_foreign_key is None:
        raise exceptions.MalformedRelationshipError(
            f"The property already defined under {fk_logical_name} does not define a "
            'foreign key constraint. Use the "x-foreign-key" extension property to '
            f'define a foreign key constraint, for example: "{foreign_key}".'
        )
    if model_foreign_key != foreign_key:
        raise exceptions.MalformedRelationshipError(
            "The foreign key required for the relationship has a different foreign "
            "key constraint than the property already defined under that name. "
            f"The required constraint is {foreign_key}. "
            f"The {fk_logical_name} property has the {model_foreign_key} constraint."
        )

    return False
