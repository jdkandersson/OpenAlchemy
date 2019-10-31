"""Database models."""

import os

from flask_sqlalchemy import SQLAlchemy

from openapi_sqlalchemy import init_yaml

db = SQLAlchemy()

models_dir = os.path.dirname(__file__)
_, model_factory = init_yaml(os.path.join(models_dir, "api.yaml"), base=db.Model)


class Employee(model_factory(name="Employee")):  # type: ignore
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
