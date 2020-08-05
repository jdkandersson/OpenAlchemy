"""Tests for link."""
# pylint: disable=protected-access

import copy
import sys

import pytest

from open_alchemy import types
from open_alchemy.column_factory import array_ref


@pytest.mark.column
def test_schemas():
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN construct is called
    THEN foreign key is not added to the referenced schema.
    """
    ref_schema = {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    artifacts = types.ObjectArtifacts(
        spec=copy.deepcopy(ref_schema),
        logical_name="ref_schema",
        fk_column="id",
        relationship=types.RelationshipArtifacts(model_name="RefSchema"),
    )
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }
    schemas = {"RefSchema": copy.deepcopy(ref_schema)}

    array_ref._link.construct(
        artifacts=artifacts, model_schema=model_schema, schemas=schemas
    )

    assert schemas == {"RefSchema": ref_schema}


@pytest.mark.column
def test_secondary(mocked_facades_models):
    """
    GIVEN schema with array referencing another schema and secondary set and schemas
    WHEN construct is called
    THEN table is set on models.
    """
    ref_schema = {
        "type": "object",
        "x-tablename": "ref_schema",
        "properties": {"id": {"type": "integer", "x-primary-key": True}},
    }
    secondary = "association"
    artifacts = types.ObjectArtifacts(
        spec=copy.deepcopy(ref_schema),
        logical_name="logical name 1",
        fk_column="id",
        relationship=types.RelationshipArtifacts(
            model_name="RefSchema", secondary=secondary
        ),
    )
    tablename = "schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer", "x-primary-key": True}},
    }
    schemas = {"RefSchema": copy.deepcopy(ref_schema)}

    array_ref._link.construct(
        artifacts=artifacts, model_schema=model_schema, schemas=schemas
    )

    assert mocked_facades_models.set_association.call_count == 1
    if sys.version_info[1] == 8:
        name = mocked_facades_models.set_association.call_args.kwargs["name"]
        table = mocked_facades_models.set_association.call_args.kwargs["table"]
    else:
        _, kwargs = mocked_facades_models.set_association.call_args
        name = kwargs["name"]
        table = kwargs["table"]
    assert name == secondary
    assert table.name == secondary
    assert schemas == {"RefSchema": ref_schema}
