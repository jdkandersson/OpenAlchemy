"""Functions relating to object references in arrays."""

import typing

import sqlalchemy

import open_alchemy
from open_alchemy import exceptions
from open_alchemy import helpers
from open_alchemy import types

from . import column
from . import object_ref


def handle_array(
    *,
    spec: types.Schema,
    model_schema: types.Schema,
    schemas: types.Schemas,
    logical_name: str,
) -> typing.Tuple[typing.List[typing.Tuple[str, typing.Type]], types.Schema]:
    """
    Generate properties for a reference to another object through an array.

    Assume that when any allOf and $ref are resolved in the root spec the type is
    array.

    Args:
        spec: The schema for the column.
        model_schema: The schema of the one to many parent.
        schemas: Used to resolve any $ref.
        logical_name: The logical name in the specification for the schema.

    Returns:
        The logical name and the relationship for the referenced object.

    """
    # Resolve any allOf and $ref
    spec = helpers.prepare_schema(schema=spec, schemas=schemas)

    # Get item specification
    item_spec = spec.get("items")
    if item_spec is None:
        raise exceptions.MalformedRelationshipError(
            "An array property must include items property."
        )
    obj_artifacts = object_ref.gather_object_artifacts(
        spec=item_spec, logical_name=logical_name, schemas=schemas
    )

    # Check for uselist
    if obj_artifacts.uselist is not None:
        raise exceptions.MalformedRelationshipError(
            "x-uselist is not supported for one to many relationships."
        )

    # Check referenced specification
    ref_spec = helpers.prepare_schema(schema=obj_artifacts.spec, schemas=schemas)
    ref_type = ref_spec.get("type")
    if ref_type != "object":
        raise exceptions.MalformedRelationshipError(
            "One to many relationships must reference an object type " "schema."
        )
    ref_tablename = helpers.get_ext_prop(source=ref_spec, name="x-tablename")
    if ref_tablename is None:
        raise exceptions.MalformedRelationshipError(
            "One to many relationships must reference a schema with "
            "x-tablename defined."
        )

    # Construct relationship
    relationship_return = (
        logical_name,
        sqlalchemy.orm.relationship(
            obj_artifacts.ref_logical_name, backref=obj_artifacts.backref
        ),
    )
    # Construct entry for the addition for the model schema
    spec_return = {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": obj_artifacts.ref_logical_name},
    }
    # Add foreign key to referenced schema
    _set_foreign_key(
        ref_model_name=obj_artifacts.ref_logical_name,
        model_schema=model_schema,
        schemas=schemas,
        fk_column=obj_artifacts.fk_column,
    )

    return [relationship_return], spec_return


def _set_foreign_key(
    *,
    ref_model_name: str,
    model_schema: types.Schema,
    schemas: types.Schemas,
    fk_column: str,
) -> None:
    """
    Set the foreign key on an existing model or add it to the schemas.

    Args:
        ref_model_name: The name of the referenced model.
        model_schema: The schema of the one to many parent.
        schemas: All the model schemas.
        fk_column: The name of the foreign key column.

    """
    # Check that model is in schemas
    if ref_model_name not in schemas:
        raise exceptions.MalformedRelationshipError(
            f"{ref_model_name} referenced in relationship was not found in the "
            "schemas."
        )

    # Calculate foreign key specification
    fk_spec = object_ref.handle_object_reference(
        spec=model_schema, schemas=schemas, fk_column=fk_column
    )

    # Calculate values for foreign key
    tablename = helpers.get_ext_prop(source=model_schema, name="x-tablename")
    fk_logical_name = f"{tablename}_{fk_column}"

    # Handle model already constructed
    ref_model = getattr(open_alchemy.models, ref_model_name, None)
    if ref_model is not None:
        # Construct foreign key
        [(_, fk_column)] = column.handle_column(
            spec=fk_spec, logical_name=fk_logical_name
        )
        setattr(ref_model, fk_logical_name, fk_column)
        return

    # Handle model not constructed
    schemas[ref_model_name] = {
        "allOf": [
            schemas[ref_model_name],
            {
                "type": "object",
                "properties": {fk_logical_name: {**fk_spec, "x-dict-ignore": True}},
            },
        ]
    }
