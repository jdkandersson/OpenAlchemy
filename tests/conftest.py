"""Fixtures for all tests."""
# pylint: disable=redefined-outer-name

import pytest
import sqlalchemy
from sqlalchemy import orm


@pytest.fixture(scope="function", params=["sqlite:///:memory:"])
def engine(request):
    """Creates a sqlite engine."""
    return sqlalchemy.create_engine(request.param)


@pytest.fixture(scope="function")
def sessionmaker(engine):
    """Creates a sqlite session."""
    return orm.sessionmaker(bind=engine)
