"""Retrieve model artifacts."""

import typing

from ... import types as oa_types
from ...helpers import ext_prop
from ...helpers import inheritance
from ...helpers import peek
from ...helpers import schema as schema_helper
from ...table_args import factory
from ..helpers import iterate
from . import types


def _calculate_backref(schema: oa_types.Schema) -> types.ModelBackrefArtifacts:
    """Calculate the backref artifact from the backref schema."""
    type_ = peek.type_(schema=schema, schemas={})
    assert type_ in {"object", "array"}

    if type_ == "object":
        parent = ext_prop.get(source=schema, name=oa_types.ExtensionProperties.DE_REF)
        assert isinstance(parent, str)
        return types.ModelBackrefArtifacts(types.BackrefSubType.OBJECT, parent)

    items_schema = peek.items(schema=schema, schemas={})
    assert items_schema is not None
    parent = ext_prop.get(source=items_schema, name=oa_types.ExtensionProperties.DE_REF)
    assert isinstance(parent, str)
    return types.ModelBackrefArtifacts(types.BackrefSubType.ARRAY, parent)


def get(
    schemas: oa_types.Schemas, schema: oa_types.Schema
) -> types.ModelExPropertiesArtifacts:
    """
    Retrieve the artifacts for the model.

    Assume that the schema is valid.

    Args:
        schema: The model schema.
        schemas: All the defined schemas used to resolve any $ref.

    Returns:
        The artifacts for the model.

    """
    tablename = peek.prefer_local(
        get_value=peek.tablename, schema=schema, schemas=schemas
    )
    assert tablename is not None
    inherits = schema_helper.inherits(schema=schema, schemas=schemas)
    parent: typing.Optional[str] = None
    if inherits is True:
        parent = inheritance.get_parent(schema=schema, schemas=schemas)

    description = peek.prefer_local(
        get_value=peek.description, schema=schema, schemas=schemas
    )

    mixins = peek.prefer_local(get_value=peek.mixins, schema=schema, schemas=schemas)

    kwargs = peek.prefer_local(get_value=peek.kwargs, schema=schema, schemas=schemas)

    composite_index: typing.Optional[oa_types.IndexList] = None
    composite_index_value = peek.prefer_local(
        get_value=peek.composite_index, schema=schema, schemas=schemas
    )
    if composite_index_value is not None:
        composite_index = factory.map_index(spec=composite_index_value)

    composite_unique: typing.Optional[oa_types.UniqueList] = None
    composite_unique_value = peek.prefer_local(
        get_value=peek.composite_unique, schema=schema, schemas=schemas
    )
    if composite_unique_value is not None:
        composite_unique = factory.map_unique(spec=composite_unique_value)

    backrefs = iterate.backrefs_items(schema=schema, schemas=schemas)
    backrefs_artifacts = map(
        lambda args: (args[0], _calculate_backref(args[1])), backrefs
    )

    return types.ModelExPropertiesArtifacts(
        tablename=tablename,
        inherits=inherits,
        parent=parent,
        description=description,
        mixins=mixins,
        kwargs=kwargs,
        composite_index=composite_index,
        composite_unique=composite_unique,
        backrefs=list(backrefs_artifacts),
    )
