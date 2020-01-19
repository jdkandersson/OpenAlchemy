"""Test for simple-example-spec.yaml."""

import pytest
from sqlalchemy.ext import declarative

import open_alchemy

from . import helpers


@pytest.mark.parametrize(
    "filename, model_name, attrs, expected_delta_attrs",
    [
        (
            "simple-example-spec.yml",
            "Employee",
            {"id": 1, "name": "name 1", "division": "division 1"},
            {"salary": None},
        ),
        (
            "simple-example-spec.yml",
            "Employee",
            {"id": 11, "name": "name 1", "division": "division 1", "salary": 12},
            {},
        ),
        (
            "all-of-column-example-spec.yml",
            "Employee",
            {"id": 11, "name": "name 1", "salary": 12},
            {},
        ),
        (
            "all-of-column-example-spec.yml",
            "Division",
            {"id": 11, "name": "name 1"},
            {},
        ),
        (
            "all-of-model-example-spec.yml",
            "Employee",
            {"id": 11, "name": "name 1", "salary": 12},
            {},
        ),
        ("all-of-model-example-spec.yml", "Division", {"id": 11, "name": "name 1"}, {}),
    ],
    ids=[
        "simple        Employee required only",
        "simple        Employee all",
        "all-of-column Employee",
        "all-of-column Division",
        "all-of-model  Employee",
        "all-of-model  Division",
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
    spec = helpers.read_spec(filename=filename)
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    model = model_factory(name=model_name)
    # Initialise database
    base.metadata.create_all(engine)
    session = sessionmaker()

    # Create instance
    model_instance = model(**attrs)
    session.add(model_instance)
    session.flush()

    queried_instances = session.query(model).first()
    expected_attrs = {**attrs, **expected_delta_attrs}
    for name, value in expected_attrs.items():
        assert getattr(queried_instances, name) == value, f"{name} != {value}"
