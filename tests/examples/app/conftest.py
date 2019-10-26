"""Fixtures for example app."""

import connexion
import pytest


@pytest.fixture(scope="session")
def app():
    """Flask app for testing."""
    # Adding swagger file
    flask_app = connexion.FlaskApp(__name__, specification_dir="../../../examples/app/")
    flask_app.add_api("api.yaml", validate_responses=True)
    # Connecting to database
    flask_app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return flask_app.app
