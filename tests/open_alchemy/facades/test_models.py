"""Tests for models facade."""

from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy.facades import models


@pytest.mark.facade
def test_get_base(mocked_models):
    """
    GIVEN mocked models
    WHEN get_base is called
    THEN the mocked_models.Base is returned.
    """
    base = models.get_base()

    assert base == mocked_models.Base


@pytest.mark.facade
def test_set_association(mocked_models):
    """
    GIVEN mocked models, mock table and name
    WHEN set_association is called with the table and name
    THEN the table is set as an attribute on the models with the name.
    """
    name = "association_1"
    table = mock.MagicMock()

    models.set_association(table=table, name=name)

    assert getattr(mocked_models, name) == table


@pytest.mark.facade
def test_get_model(mocked_models):
    """
    GIVE mocked models and name
    WHEN get_model is called with the name
    THEN the models attribute with that name is returned.
    """
    name = "Model"

    model = models.get_model(name=name)

    assert model == getattr(mocked_models, name)


@pytest.mark.facade
def test_get_not_defined(mocked_models):
    """
    GIVE mocked models without model and name
    WHEN get_model is called with the name
    THEN None is returned.
    """
    name = "Model"
    del mocked_models.Model

    model = models.get_model(name=name)

    assert model is None


@pytest.mark.facade
def test_set_model(mocked_models):
    """
    GIVE mocked models, mock model and name
    WHEN set_model is called with the model and name
    THEN the model is set as an attribute on the models with the name.
    """
    model = mock.MagicMock()
    name = "Model"

    models.set_model(model=model, name=name)

    assert getattr(mocked_models, name) == model


class TestAddBackrefToModel:
    """Tests for _add_backref_to_model."""

    #  pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "schema, expected_schema",
        [
            (
                {},
                {
                    "x-backrefs": {
                        "ref_schema": {"type": "object", "x-de-$ref": "RefSchema"}
                    }
                },
            ),
            (
                {"x-backrefs": {}},
                {
                    "x-backrefs": {
                        "ref_schema": {"type": "object", "x-de-$ref": "RefSchema"}
                    }
                },
            ),
            (
                {
                    "x-backrefs": {
                        "ref_schema1": {"type": "object", "x-de-$ref": "RefSchema1"}
                    }
                },
                {
                    "x-backrefs": {
                        "ref_schema1": {"type": "object", "x-de-$ref": "RefSchema1"},
                        "ref_schema": {"type": "object", "x-de-$ref": "RefSchema"},
                    }
                },
            ),
            (
                {
                    "x-backrefs": {
                        "ref_schema1": {"type": "object", "x-de-$ref": "RefSchema1"},
                        "ref_schema2": {"type": "object", "x-de-$ref": "RefSchema2"},
                    }
                },
                {
                    "x-backrefs": {
                        "ref_schema1": {"type": "object", "x-de-$ref": "RefSchema1"},
                        "ref_schema2": {"type": "object", "x-de-$ref": "RefSchema2"},
                        "ref_schema": {"type": "object", "x-de-$ref": "RefSchema"},
                    }
                },
            ),
        ],
        ids=[
            "x-backrefs missing",
            "x-backrefs empty",
            "x-backrefs single",
            "x-backrefs multiple",
        ],
    )
    @pytest.mark.facade
    def test_valid(schema, expected_schema):
        """
        GIVEN given schema and backref to add
        WHEN _add_backref_to_model is called with the schema and backref to add
        THEN the backref is added to the schema.
        """
        # pylint: disable=protected-access
        backref = {"type": "object", "x-de-$ref": "RefSchema"}
        property_name = "ref_schema"

        models._add_backref_to_model(
            schema=schema, backref=backref, property_name=property_name
        )

        assert schema == expected_schema

    @staticmethod
    @pytest.mark.facade
    def test_invalid():
        """
        GIVEN given schema with invalid x-backrefs
        WHEN _add_backref_to_model is called with the schema
        THEN MalformedExtensionPropertyError is raised.
        """
        schema = {"x-backrefs": ["invalid"]}

        with pytest.raises(exceptions.MalformedExtensionPropertyError):
            models._add_backref_to_model(
                schema=schema, backref={}, property_name="ref_schema"
            )


class TestAddBackrefToSchemas:
    """Tests for _add_backref_to_schemas."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    def test_miss():
        """
        GIVEN empty schemas
        WHEN _add_backref_to_schemas is called
        THEN SchemaNotFoundError is raised.
        """
        with pytest.raises(exceptions.SchemaNotFoundError):
            models._add_backref_to_schemas(
                name="Schema", schemas={}, backref={}, property_name="ref_schema"
            )

    @staticmethod
    @pytest.mark.parametrize(
        "schemas",
        [
            {"RefSchema": {"type": "object", "properties": {}}},
            {"RefSchema": {"allOf": [{"type": "object", "properties": {}}]}},
        ],
        ids=["plain", "allOf exists"],
    )
    @pytest.mark.facade
    def test_valid(schemas):
        """
        GIVEN given given name, schemas and backref
        WHEN _add_backref_to_schemas is called with the name, schemas and backref
        THEN the backref is added to the schemas.
        """
        backref = {"type": "object", "x-de-$ref": "Schema"}
        name = "RefSchema"

        models._add_backref_to_schemas(
            name=name, schemas=schemas, backref=backref, property_name="ref_schema"
        )

        assert schemas == {
            "RefSchema": {
                "allOf": [
                    {"type": "object", "properties": {}},
                    {
                        "type": "object",
                        "x-backrefs": {
                            "ref_schema": {"type": "object", "x-de-$ref": "Schema"}
                        },
                    },
                ]
            }
        }


@pytest.mark.facade
def test_add_backref_model_defined(mocked_models):
    """
    GIVEN mocked models with model defined and backref schema
    WHEN add_backref is called
    THEN the backref schema is added to the model.
    """
    model = mocked_models.RefModel
    model._schema = {}  # pylint: disable=protected-access
    backref = {"type": "object", "x-de-$ref": "Model"}

    models.add_backref(
        name="RefModel", schemas={}, backref=backref, property_name="model"
    )

    assert model._schema == {  # pylint: disable=protected-access
        "x-backrefs": {"model": {"type": "object", "x-de-$ref": "Model"}}
    }


@pytest.mark.facade
def test_add_backref_model_not_defined(mocked_models):
    """
    GIVEN mocked models with model not defined and backref schema
    WHEN add_backref is called
    THEN the backref schema is added to the model.
    """
    del mocked_models.RefModel
    schemas = {"RefModel": {"type": "object", "properties": {}}}
    backref = {"type": "object", "x-de-$ref": "Model"}

    models.add_backref(
        name="RefModel", schemas=schemas, backref=backref, property_name="model"
    )

    assert schemas == {
        "RefModel": {
            "allOf": [
                {"type": "object", "properties": {}},
                {
                    "type": "object",
                    "x-backrefs": {"model": {"type": "object", "x-de-$ref": "Model"}},
                },
            ]
        }
    }
