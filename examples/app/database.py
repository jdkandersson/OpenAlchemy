"""Setup for the database."""

import os

from flask_sqlalchemy import SQLAlchemy

from openapi_sqlalchemy import init_yaml

db = SQLAlchemy()
models_dir = os.path.dirname(__file__)
models_file = os.path.join(models_dir, "api.yaml")
init_yaml(models_file, base=db.Model)
