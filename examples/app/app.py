"""Application code."""

import os

import connexion

import db
from openapi_sqlalchemy import init_yaml

# Creating Flask app
app = connexion.FlaskApp(__name__, specification_dir=".")

# Initializing database
app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.db.init_app(app.app)

# Creating models
models_dir = os.path.dirname(__file__)
models_file = os.path.join(models_dir, "api.yaml")
init_yaml(models_file, base=db.Model)

with app.app.app_context():
    db.db.create_all()
app.add_api("api.yaml")
app.run(port=8080)
