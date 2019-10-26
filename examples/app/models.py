"""Database models."""

import os

from flask_sqlalchemy import SQLAlchemy
from yaml import safe_load

from openapi_sqlalchemy import init_model_factory

db = SQLAlchemy()

models_dir = os.path.dirname(__file__)
with open(os.path.join(models_dir, "api.yaml")) as spec_file:
    SPEC = safe_load(spec_file)
MODEL_FACTORY = init_model_factory(base=db.Model, spec=SPEC)


class Employee(MODEL_FACTORY(name="Employee")):  # type: ignore
    """Employee model with conversion to and from dictionaries."""

    @classmethod
    def from_dict(cls, body):
        """Convert a dictionary to an Employee."""
        return cls(**body)

    def to_dict(self):
        """Convert Employee to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "division": self.division,
            "salary": self.salary,
        }
