"""Tests for models."""
# pylint: disable=protected-access

import pytest

from open_alchemy import models_file

DOCSTRING = '"""SQLAlchemy models based on models constructed by OpenAlchemy."""'


@pytest.mark.parametrize(
    "models, expected_source",
    [
        (
            ["model 1"],
            f"""{DOCSTRING}
# pylint: disable=no-member

from open_alchemy import models
model 1
""",
        ),
        (
            ["model 1", "model 2"],
            f"""{DOCSTRING}
# pylint: disable=no-member

from open_alchemy import models
model 1
model 2
""",
        ),
        (
            ["model 1 typing."],
            f"""{DOCSTRING}
# pylint: disable=no-member

import typing

from open_alchemy import models
model 1 typing.
""",
        ),
        (
            ["model 1 datetime."],
            f"""{DOCSTRING}
# pylint: disable=no-member

import datetime

from open_alchemy import models
model 1 datetime.
""",
        ),
        (
            ["model 1 typing. datetime."],
            f"""{DOCSTRING}
# pylint: disable=no-member

import datetime
import typing

from open_alchemy import models
model 1 typing. datetime.
""",
        ),
    ],
    ids=[
        "single model",
        "multiple models",
        "contains typing",
        "contains datetime",
        "contains multiple imports",
    ],
)
@pytest.mark.models_file
def test_generate(models, expected_source):
    """
    GIVEN single model
    WHEN generate is called
    THEN the source for the models file is returned.
    """
    source = models_file._models.generate(models=models)

    assert source == expected_source
