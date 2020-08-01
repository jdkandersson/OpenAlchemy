"""Tests for full relationship schema checking."""

import pytest

from open_alchemy.schemas.validation.relationship import full


@pytest.mark.parametrize(
    "schemas, source_schema, property_schema, expected_result",
    [
        pytest.param(id="x-to-one referenced schema no tablenamed"),
        pytest.param(id="x-to-one foreign key default not present"),
        pytest.param(id="x-to-one foreign key default present"),
        pytest.param(id="x-to-one foreign key configured not present"),
        pytest.param(id="x-to-one foreign key configured present"),
        pytest.param(id="x-to-one foreign key property invalid"),
        pytest.param(id="x-to-one foreign key property valid"),
        pytest.param(id="x-to-one foreign key defined different type"),
        pytest.param(id="x-to-one foreign key defined same type"),
        pytest.param(id="x-to-one foreign key defined different format"),
        pytest.param(id="x-to-one foreign key defined same format"),
        pytest.param(id="x-to-one foreign key defined different maxLength"),
        pytest.param(id="x-to-one foreign key defined same maxLength"),
        pytest.param(id="x-to-one foreign key defined different default"),
        pytest.param(id="x-to-one foreign key defined same default"),
        pytest.param(id="x-to-one foreign key defined wrong foreign key"),
        pytest.param(id="x-to-one foreign key defined right foreign key"),
        pytest.param(id="one-to-many source schema no tablenamed"),
        pytest.param(id="one-to-many foreign key default not present"),
        pytest.param(id="one-to-many foreign key default present"),
        pytest.param(id="one-to-many foreign key configured not present"),
        pytest.param(id="one-to-many foreign key configured present"),
        pytest.param(id="one-to-many foreign key property invalid"),
        pytest.param(id="one-to-many foreign key property valid"),
        pytest.param(id="one-to-many foreign key defined different type"),
        pytest.param(id="one-to-many foreign key defined same type"),
        pytest.param(id="one-to-many foreign key defined different format"),
        pytest.param(id="one-to-many foreign key defined same format"),
        pytest.param(id="one-to-many foreign key defined different maxLength"),
        pytest.param(id="one-to-many foreign key defined same maxLength"),
        pytest.param(id="one-to-many foreign key defined different default"),
        pytest.param(id="one-to-many foreign key defined same default"),
        pytest.param(id="one-to-many foreign key defined wrong foreign key"),
        pytest.param(id="one-to-many foreign key defined right foreign key"),
        pytest.param(id="many-to-many source no tablename"),
        pytest.param(id="many-to-many referenced no tablename"),
        pytest.param(id="many-to-many source no primary key property"),
        pytest.param(id="many-to-many source invalid primary key property"),
        pytest.param(id="many-to-many source multiple primary key property"),
        pytest.param(id="many-to-many referenced no primary key property"),
        pytest.param(id="many-to-many referenced invalid primary key property"),
        pytest.param(id="many-to-many referenced multiple primary key property"),
        pytest.param(id="many-to-many valid"),
    ],
)
@pytest.mark.schemas
def test_check(schemas, source_schema, property_schema, expected_result):
    """
    GIVEN schemas, the source and property schema and the expected result
    WHEN check is called with the schemas and source and property schema
    THEN the expected result is returned.
    """
    # pylint: disable=assignment-from-no-return
    returned_result = full.check(schemas, source_schema, property_schema)

    assert returned_result == expected_result
