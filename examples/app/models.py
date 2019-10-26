"""Database models."""

from flask_sqlalchemy import SQLAlchemy
from yaml import safe_load

from openapi_sqlalchemy import init_model_factory

db = SQLAlchemy()

with open("api.yaml") as spec_file:
    SPEC = safe_load(spec_file)
MODEL_FACTORY = init_model_factory(base=db.Model, spec=SPEC)


class Employee(MODEL_FACTORY(name="Employee")):
    """Employee model with serialization function."""

    def to_dict(self):
        """Convert Employee to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "division": self.division,
            "salary": self.salary,
        }
