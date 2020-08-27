"""Retrieve artifacts for a relationship property."""

import typing

from .... import helpers as oa_helpers
from .... import types as oa_types
from ... import helpers
from .. import types


def _get_parent(*, schema: oa_types.Schema, schemas: oa_types.Schemas) -> str:
    """Retrieve the parent name from an object reference."""
    ref = oa_helpers.peek.ref(schema=schema, schemas=schemas)
    assert ref is not None
    parent, _ = oa_helpers.ref.get_ref(ref=ref, schemas=schemas)
    return parent


def _calculate_x_to_one_schema(
    *, parent: str, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> oa_types.ObjectRefSchema:
    """Calculate the schema for a x-to-one relationship."""
    return_schema: oa_types.ObjectRefSchema = {"type": "object", "x-de-$ref": parent}

    description = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.description, schema=schema, schemas=schemas
    )
    if description is not None:
        return_schema["description"] = description
    nullable = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.nullable, schema=schema, schemas=schemas
    )
    if nullable is not None:
        return_schema["nullable"] = nullable
    write_only = oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.write_only, schema=schema, schemas=schemas
    )
    if write_only is not None:
        return_schema["writeOnly"] = write_only

    return return_schema


def _get_backref_property(
    *, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> typing.Optional[str]:
    """Retrieve the backref from an object reference."""
    return oa_helpers.peek.prefer_local(
        get_value=oa_helpers.peek.backref, schema=schema, schemas=schemas
    )


def _get_kwargs(
    *, parent: str, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """Retrieve the kwargs name from an object reference."""
    return oa_helpers.peek.peek_key(
        schema=schema, schemas=schemas, key="x-kwargs", skip_ref=parent
    )


def _get_write_only(
    *, parent: str, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> typing.Optional[bool]:
    """Retrieve the writeOnly value from a schema."""
    return oa_helpers.peek.peek_key(
        schema=schema, schemas=schemas, key="writeOnly", skip_ref=parent
    )


def _get_many_to_one(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a many-to-one relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    parent = _get_parent(schema=schema, schemas=schemas)

    return types.ManyToOneRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.MANY_TO_ONE,
        schema=_calculate_x_to_one_schema(
            parent=parent, schema=schema, schemas=schemas
        ),
        required=None,
        parent=parent,
        backref_property=_get_backref_property(schema=schema, schemas=schemas),
        kwargs=_get_kwargs(parent=parent, schema=schema, schemas=schemas),
        write_only=_get_write_only(parent=parent, schema=schema, schemas=schemas),
        description=None,
        foreign_key="",
        foreign_key_property="",
        nullable=None,
    )


def _get_one_to_one(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a one-to-one relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    parent = _get_parent(schema=schema, schemas=schemas)

    return types.OneToOneRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.ONE_TO_ONE,
        schema=_calculate_x_to_one_schema(
            parent=parent, schema=schema, schemas=schemas
        ),
        required=None,
        parent=parent,
        backref_property=_get_backref_property(schema=schema, schemas=schemas),
        kwargs=_get_kwargs(parent=parent, schema=schema, schemas=schemas),
        write_only=_get_write_only(parent=parent, schema=schema, schemas=schemas),
        description=None,
        foreign_key="",
        foreign_key_property="",
        nullable=None,
    )


def _calculate_one_to_x_schema(
    *, parent: str, schema: oa_types.Schema, schemas: oa_types.Schemas
) -> oa_types.ArrayRefSchema:
    """Calculate the schema for a x-to-one relationship."""
    return_schema: oa_types.ArrayRefSchema = {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": parent},
    }

    description = oa_helpers.peek.description(schema=schema, schemas=schemas)
    if description is not None:
        return_schema["description"] = description
    write_only = oa_helpers.peek.write_only(schema=schema, schemas=schemas)
    if write_only is not None:
        return_schema["writeOnly"] = write_only

    return return_schema


def _get_one_to_many(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a one-to-many relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    assert items_schema is not None

    parent = _get_parent(schema=items_schema, schemas=schemas)

    return types.OneToManyRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.ONE_TO_MANY,
        schema=_calculate_one_to_x_schema(
            parent=parent, schema=schema, schemas=schemas
        ),
        required=None,
        parent=parent,
        backref_property=_get_backref_property(schema=items_schema, schemas=schemas),
        kwargs=_get_kwargs(parent=parent, schema=items_schema, schemas=schemas),
        write_only=_get_write_only(parent=parent, schema=schema, schemas=schemas),
        description=None,
        foreign_key="",
        foreign_key_property="",
    )


def _get_many_to_many(*, schema: oa_types.Schema, schemas: oa_types.Schemas):
    """
    Retrieve the artifacts for a many-to-many relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.

    Returns:
        The artifacts for the property.

    """
    items_schema = oa_helpers.peek.items(schema=schema, schemas=schemas)
    assert items_schema is not None

    parent = _get_parent(schema=items_schema, schemas=schemas)

    return types.ManyToManyRelationshipPropertyArtifacts(
        type_=helpers.property_.type_.Type.RELATIONSHIP,
        sub_type=oa_helpers.relationship.Type.MANY_TO_MANY,
        schema=_calculate_one_to_x_schema(
            parent=parent, schema=schema, schemas=schemas
        ),
        required=None,
        parent=parent,
        backref_property=_get_backref_property(schema=items_schema, schemas=schemas),
        kwargs=_get_kwargs(parent=parent, schema=items_schema, schemas=schemas),
        write_only=_get_write_only(parent=parent, schema=schema, schemas=schemas),
        description=None,
        secondary="secondary",
    )


_GET_MAPPING = {
    oa_helpers.relationship.Type.MANY_TO_ONE: _get_many_to_one,
    oa_helpers.relationship.Type.ONE_TO_ONE: _get_one_to_one,
    oa_helpers.relationship.Type.ONE_TO_MANY: _get_one_to_many,
    oa_helpers.relationship.Type.MANY_TO_MANY: _get_many_to_many,
}


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema, required: bool
) -> types.TAnyRelationshipPropertyArtifacts:
    """
    Retrieve the artifacts for a relationship property.

    Args:
        schemas: All the defined schemas.
        schema: The schema of the relationship property to gather artifacts for.
        required: WHether the property appears in the required list.

    Returns:
        The artifacts for the property.

    """
    sub_type = oa_helpers.relationship.calculate_type(schema=schema, schemas=schemas)

    artifacts = _GET_MAPPING[sub_type](schema=schema, schemas=schemas)
    artifacts.required = required

    return artifacts
