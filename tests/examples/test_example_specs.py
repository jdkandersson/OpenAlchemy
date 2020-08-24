"""Test for examples."""

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
        pytest.param(
            "simple/example-spec.yml",
            "Employee",
            {"name": "employee 1", "division": "division 1"},
            {"id": 1, "salary": None},
            id="simple Employee required only",
        ),
        pytest.param(
            "simple/example-spec.yml",
            "Employee",
            {"id": 11, "name": "employee 1", "division": "division 1", "salary": 12},
            {},
            id="simple Employee all",
        ),
        pytest.param(
            "all_of/column-example-spec.yml",
            "Employee",
            {"id": 11, "name": "employee 1", "salary": 12},
            {},
            id="all-of-column Employee",
        ),
        pytest.param(
            "all_of/column-example-spec.yml",
            "Division",
            {"id": 11, "name": "employee 1"},
            {},
            id="all-of-column Division",
        ),
        pytest.param(
            "all_of/model-example-spec.yml",
            "Employee",
            {"id": 11, "name": "employee 1", "salary": 12},
            {},
            id="all-of-model Employee",
        ),
        pytest.param(
            "all_of/model-example-spec.yml",
            "Division",
            {"id": 11, "name": "employee 1"},
            {},
            id="all-of-model Division",
        ),
        pytest.param(
            "composite_index/example-spec.yml",
            "Employee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
            id="composite-index Employee",
        ),
        pytest.param(
            "ref/column-example-spec.yml",
            "Employee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
            id="ref-column Employee",
        ),
        pytest.param(
            "ref/model-example-spec.yml",
            "RefEmployee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
            id="ref-model Employee",
        ),
        pytest.param(
            "composite_unique/example-spec.yml",
            "Employee",
            {"id": 1, "name": "employee 1", "division": "division 1"},
            {},
            id="unique-constraint Employee",
        ),
        pytest.param(
            "default/example-spec.yml",
            "Employee",
            {"id": 1},
            {"name": "Unknown"},
            id="default Employee",
        ),
        pytest.param(
            "read_only/example-spec.yml",
            "Employee",
            {"name": "name 1"},
            {"id": 1, "name": "name 1"},
            id="read_only Employee",
        ),
        pytest.param(
            "json/example-spec.yml",
            "Employee",
            {"name": "name 1", "division": "division 1", "data": {"key": "value"}},
            {
                "id": 1,
                "name": "name 1",
                "division": "division 1",
                "data": {"key": "value"},
            },
            id="json Employee",
        ),
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


@pytest.mark.example
def test_single_model_write_only(engine, sessionmaker):
    """
    GIVEN writeOnly example spec
    WHEN model instance is created with the input dictionary
    THEN the writeOnly field is not returned when it is converted to a dictionary.
    """
    filename = "write_only/example-spec.yml"
    model_name = "Employee"
    employee_dict = {"name": "name 1", "passport_number": "passport number 1"}
    model, session = helpers.create_model_session(
        filename=filename,
        model_name=model_name,
        engine=engine,
        sessionmaker=sessionmaker,
    )

    # Create instance
    model_instance = model(**employee_dict)
    session.add(model_instance)
    session.flush()

    queried_instance = session.query(model).first()
    assert queried_instance.passport_number == "passport number 1"
    assert queried_instance.to_dict() == {"id": 1, "name": "name 1"}


@pytest.mark.example
def test_single_model_mixins(engine, sessionmaker):
    """
    GIVEN example spec with mixins
    WHEN model instance is created with the input dictionary
    THEN the mixins are added to the model.
    """
    filename = "mixins/example-spec.yml"
    model_name = "Employee"
    employee_dict = {"name": "employee 1", "division": "division 1"}
    model, session = helpers.create_model_session(
        filename=filename,
        model_name=model_name,
        engine=engine,
        sessionmaker=sessionmaker,
    )

    # Create instance
    model_instance = model(**employee_dict)
    session.add(model_instance)
    session.flush()

    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == {
        "division": "division 1",
        "id": 1,
        "name": "employee 1",
    }
    assert hasattr(queried_instance, "created_at")
    assert hasattr(queried_instance, "updated_at")


@pytest.mark.parametrize(
    "filename, model_name, sql, expected_contents",
    [
        (
            "simple/example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE name='employee'",
            ["PRIMARY KEY (id)"],
        ),
        (
            "simple/example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE type='index'",
            [
                "INDEX ix_employee_name ON employee (name)",
                "INDEX ix_employee_division ON employee (division)",
            ],
        ),
        (
            "composite_index/example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE type='index'",
            ["INDEX ix_employee_name ON employee (name, division)"],
        ),
        (
            "composite_unique/example-spec.yml",
            "Employee",
            "SELECT sql FROM sqlite_master WHERE name='employee'",
            ["UNIQUE (address, division)"],
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
        pytest.param(
            "relationship/many_to_one/example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
            id="relationship-many-to-one",
        ),
        pytest.param(
            "relationship/many_to_one/backref-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
            id="relationship-many-to-one-backref",
        ),
        pytest.param(
            "relationship/many_to_one/custom-foreign-key-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
            id="relationship-many-to-one-custom-foreign-key",
        ),
        pytest.param(
            "relationship/many_to_one/not-nullable-example-spec.yml",
            ("Employee", "Division"),
            {
                "id": 11,
                "name": "employee 1",
                "division": {"id": 12, "name": "division 1"},
            },
            id="relationship-many-to-one-not-nullable",
        ),
        pytest.param(
            "relationship/one_to_many/example-spec.yml",
            ("Division", "Employee"),
            {
                "id": 11,
                "name": "division 1",
                "employees": [{"id": 12, "name": "employee 1"}],
            },
            id="relationship-one-to-many",
        ),
        pytest.param(
            "relationship/one_to_one/example-spec.yml",
            ("Employee", "PayInfo"),
            {
                "id": 11,
                "name": "employee 1",
                "pay_info": {"id": 12, "account_number": "account 1"},
            },
            id="relationship-one-to-one",
        ),
        pytest.param(
            "relationship/many_to_many/example-spec.yml",
            ("Employee", "Project"),
            {
                "id": 11,
                "name": "employee 1",
                "projects": [{"id": 12, "name": "project 1"}],
            },
            id="relationship-many-to-many",
        ),
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


@pytest.mark.parametrize(
    "filename, model_names, attrs, test_idx",
    [
        (
            "inheritance/single-example-spec.yml",
            ("Employee", "Manager", "Engineer"),
            {"id": 1, "name": "employee 1", "type": "employee"},
            0,
        ),
        (
            "inheritance/single-example-spec.yml",
            ("Employee", "Manager", "Engineer"),
            {
                "id": 1,
                "name": "employee 1",
                "type": "manager",
                "manager_data": "manager data 1",
            },
            1,
        ),
        (
            "inheritance/single-example-spec.yml",
            ("Employee", "Manager", "Engineer"),
            {
                "id": 1,
                "name": "employee 1",
                "type": "engineer",
                "engineer_info": "engineer info 1",
            },
            2,
        ),
        (
            "inheritance/joined-example-spec.yml",
            ("Employee", "Manager", "Engineer"),
            {"id": 1, "name": "employee 1", "type": "employee"},
            0,
        ),
        (
            "inheritance/joined-example-spec.yml",
            ("Employee", "Manager", "Engineer"),
            {
                "id": 1,
                "name": "employee 1",
                "type": "manager",
                "manager_data": "manager data 1",
            },
            1,
        ),
        (
            "inheritance/joined-example-spec.yml",
            ("Employee", "Manager", "Engineer"),
            {
                "id": 1,
                "name": "employee 1",
                "type": "engineer",
                "engineer_info": "engineer info 1",
            },
            2,
        ),
    ],
    ids=[
        "single Employee",
        "single Manager",
        "single Engineer",
        "joined Employee",
        "joined Manager",
        "joined Engineer",
    ],
)
@pytest.mark.example
def test_inheritance(engine, sessionmaker, filename, model_names, attrs, test_idx):
    """
    GIVEN spec with inheritance
    WHEN model is constructed and passed to the database
    THEN the constructed data is returned when queried.
    """
    test_models, session = helpers.create_models_session(
        filename=filename,
        model_names=model_names,
        engine=engine,
        sessionmaker=sessionmaker,
    )
    model = test_models[test_idx]

    # Create instance
    model_instance = model.from_dict(**attrs)
    session.add(model_instance)
    session.flush()

    queried_instance = session.query(model).first()
    assert queried_instance.to_dict() == attrs
