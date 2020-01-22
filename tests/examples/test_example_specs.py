"""Test for simple-example-spec.yaml."""

import pytest

from open_alchemy import models

from . import helpers


@pytest.fixture(autouse=True)
def cleanup_models():
    """Remove any new attributes on open_alchemy.models."""
    for key in set(models.__dict__.keys()):
        if key.startswith("__"):
            continue
        if key.endswith("__"):
            continue
        delattr(models, key)

    yield

    for key in set(models.__dict__.keys()):
        if key.startswith("__"):
            continue
        if key.endswith("__"):
            continue
        delattr(models, key)


@pytest.mark.parametrize(
    "filename, model_name, attrs, expected_delta_attrs",
    [
        (
            "simple-example-spec.yml",
            "Employee",
            {"name": "employee 1", "division": "division 1"},
            {"id": 1, "salary": None},
        ),
        (
            "simple-example-spec.yml",
            "Employee",
            {"id": 11, "name": "employee 1", "division": "division 1", "salary": 12},
            {},
        ),
        (
            "all-of-column-example-spec.yml",
            "Employee",
            {"id": 11, "name": "employee 1", "salary": 12},
            {},
        ),
        (
            "all-of-column-example-spec.yml",
            "Division",
            {"id": 11, "name": "employee 1"},
            {},
        ),
        (
            "all-of-model-example-spec.yml",
            "Employee",
            {"id": 11, "name": "employee 1", "salary": 12},
            {},
        ),
        (
            "all-of-model-example-spec.yml",
            "Division",
            {"id": 11, "name": "employee 1"},
            {},
        ),
        (
            "composite-index-example-spec.yml",
            "Employee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
        ),
        (
            "ref-column-example-spec.yml",
            "Employee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
        ),
        (
            "ref-model-example-spec.yml",
            "RefEmployee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
        ),
        (
            "unique-constraint-example-spec.yml",
            "Employee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
        ),
    ],
    ids=[
        "simple            Employee required only",
        "simple            Employee all",
        "all-of-column     Employee",
        "all-of-column     Division",
        "all-of-model      Employee",
        "all-of-model      Division",
        "composite-index   Employee",
        "ref-column        Employee",
        "ref-model         Employee",
        "unique-constraint Employee",
    ],
)
@pytest.mark.example
def test_single_model(
    engine, sessionmaker, filename, model_name, attrs, expected_delta_attrs
):
    """
    GIVEN example spec filename, model name and attrs for model instance creation
    WHEN model instance is created with the attrs and sent to the database
    THEN the attrs modified with given delta attrs is returned when the database is
        queried.
    """
    model, session = helpers.create_model_session(
        filename=filename,
        model_name=model_name,
        engine=engine,
        sessionmaker=sessionmaker,
    )

    # Create instance
    model_instance = model(**attrs)
    session.add(model_instance)
    session.flush()

    queried_instance = session.query(model).first()
    expected_attrs = {**attrs, **expected_delta_attrs}
    for name, value in expected_attrs.items():
        assert getattr(queried_instance, name) == value, f"{name} != {value}"


@pytest.mark.parametrize(
    "filename, model_name, sql, expected_contents",
    [
        (
            "simple-example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE name='employee'",
            ["PRIMARY KEY (id)"],
        ),
        (
            "simple-example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE type='index'",
            [
                "INDEX ix_employee_name ON employee (name)",
                "INDEX ix_employee_division ON employee (division)",
            ],
        ),
        (
            "composite-index-example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE type='index'",
            ["INDEX ix_employee_name ON employee (name, division)"],
        ),
        (
            "unique-constraint-example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE name='employee'",
            ["UNIQUE (division, address)"],
        ),
    ],
    ids=[
        "simple            Employee primary key",
        "simple            Employee indexes",
        "composite-index   Employee indexes",
        "unique-constraint Employee indexes",
    ],
)
@pytest.mark.example
def test_table_args(engine, filename, model_name, sql, expected_contents):
    """
    GIVEN spec, model name, sql to execute and expected contents
    WHEN models are constructed
    THEN when sql is executed the expected contents are in the result.
    """
    helpers.create_model(filename=filename, model_name=model_name, engine=engine)

    # Query schema
    results_list = list(str(result) for result in engine.execute(sql))
    results = "\n".join(results_list)

    for expected_content in expected_contents:
        assert expected_content in results


@pytest.mark.parametrize(
    "filename, model_names, attrs",
    [
        (
            "relationship-many-to-one-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
        ),
        (
            "relationship-many-to-one-backref-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
        ),
        (
            "relationship-many-to-one-custom-foreign-key-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
        ),
        (
            "relationship-many-to-one-not-nullable-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
        ),
        (
            "relationship-one-to-many-example-spec.yml",
            ("Division", "Employee"),
            {
                "id": 11,
                "name": "division 1",
                "employees": [{"id": 12, "name": "employee 1"}],
            },
        ),
        (
            "relationship-one-to-one-example-spec.yml",
            ("Employee", "PayInfo"),
            {
                "id": 11,
                "name": "employee 1",
                "pay_info": {"id": 12, "account_number": "account 1"},
            },
        ),
        (
            "relationship-many-to-many-example-spec.yml",
            ("Employee", "Project"),
            {
                "id": 11,
                "name": "employee 1",
                "projects": [{"id": 12, "name": "project 1"}],
            },
        ),
    ],
    ids=[
        "relationship-many-to-one",
        "relationship-many-to-one-backref",
        "relationship-many-to-one-custom-foreign-key",
        "relationship-many-to-one-not-nullable",
        "relationship-one-to-many",
        "relationship-one-to-one",
        "relationship-many-to-many",
    ],
)
@pytest.mark.example
def test_relationship(engine, sessionmaker, filename, model_names, attrs):
    """
    GIVEN spec with relationship
    WHEN model is constructed and passed to the database
    THEN the constructed data is returned when queried.
    """
    test_models, session = helpers.create_models_session(
        filename=filename,
        model_names=model_names,
        engine=engine,
        sessionmaker=sessionmaker,
    )
    model = test_models[0]

    # Create instance
    model_instance = model.from_dict(**attrs)
    session.add(model_instance)
    session.flush()

    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == attrs
