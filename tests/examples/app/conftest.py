"""Fixtures for example app."""

import sys

import connexion
import pytest

from examples.app import models


@pytest.fixture(scope="session")
def app():
    """Flask app for testing."""
    # Adding app directory to path
    sys.path.append("examples/app/")
    # Adding swagger file
    flask_app = connexion.FlaskApp(__name__, specification_dir="../../../examples/app/")
    flask_app.add_api("api.yaml", validate_responses=True)
    # Connecting to database
    flask_app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return flask_app.app


@pytest.fixture(scope="session")
def _db(app):  # pylint: disable=redefined-outer-name
    """Database session for testing"""
    models.db.init_app(app)
    models.db.app = app
    models.db.create_all()
    return models.db


@pytest.fixture(autouse=True)
def cleanup(db_session):
    """Clean out Employees."""
    db_session.query(models.Employee).delete()
    db_session.commit()

    yield

    db_session.query(models.Employee).delete()
    db_session.commit()
