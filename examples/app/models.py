"""Database models."""

import os

from flask_sqlalchemy import SQLAlchemy

from openapi_sqlalchemy import init_yaml

db = SQLAlchemy()

models_dir = os.path.dirname(__file__)
_, model_factory = init_yaml(os.path.join(models_dir, "api.yaml"), base=db.Model)


Employee = model_factory(name="Employee")
