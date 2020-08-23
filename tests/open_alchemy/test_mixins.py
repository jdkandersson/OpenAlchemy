"""Tests for mixins."""

import importlib
from unittest import mock

import pytest

from open_alchemy import exceptions
from open_alchemy import mixins


@pytest.mark.mixins
def test_single_import_error(monkeypatch):
    """
    GIVEN single mixins and mocked importlib with import_module that raises ImportError
    WHEN get is called with the mixins
    THEN MalformedExtensionPropertyError is raised.
    """
    mock_import_module = mock.MagicMock()
    mock_import_module.side_effect = ImportError
    monkeypatch.setattr(importlib, "import_module", mock_import_module)
    mixin_values = ["module.Mixin1"]

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        mixins.get(mixins=mixin_values)


@pytest.mark.mixins
def test_single_attribute_missing(monkeypatch):
    """
    GIVEN single mixins and mocked importlib that returns a module that doesn't have
        the class
    WHEN get is called with the mixins
    THEN MalformedExtensionPropertyError is raised.
    """
    mock_import_module = mock.MagicMock()
    del mock_import_module.return_value.Mixin1
    monkeypatch.setattr(importlib, "import_module", mock_import_module)
    mixin_values = ["module.Mixin1"]

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        mixins.get(mixins=mixin_values)


@pytest.mark.mixins
def test_single_attribute_not_class(monkeypatch):
    """
    GIVEN single mixins and mocked importlib that returns a module where the value is
        not a class
    WHEN get is called with the mixins
    THEN MalformedExtensionPropertyError is raised.
    """
    mock_import_module = mock.MagicMock()
    mixin_class = "Mixin1"
    mock_import_module.return_value.Mixin1 = mixin_class
    monkeypatch.setattr(importlib, "import_module", mock_import_module)
    mixin_values = ["module.Mixin1"]

    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        mixins.get(mixins=mixin_values)


@pytest.mark.parametrize(
    "mixin_value, expected_call_arg",
    [
        pytest.param("parent_module.Mixin1", "parent_module", id="parent module"),
        pytest.param(
            "parent_module.child_module.Mixin1",
            "parent_module.child_module",
            id="child module",
        ),
    ],
)
@pytest.mark.mixins
def test_single_valid(mixin_value, expected_call_arg, monkeypatch):
    """
    GIVEN single mixins and mocked importlib
    WHEN get is called with the mixins
    THEN the attribute is retrieved from the imported module.
    """
    mock_import_module = mock.MagicMock()
    mixin_class = type("Mixin1", (), {})
    mock_import_module.return_value.Mixin1 = mixin_class
    monkeypatch.setattr(importlib, "import_module", mock_import_module)
    mixin_values = [mixin_value]

    returned_mixin_classes = mixins.get(mixins=mixin_values)

    assert returned_mixin_classes == (mixin_class,)
    mock_import_module.assert_called_once_with(expected_call_arg)


@pytest.mark.mixins
def test_multiple_valid(monkeypatch):
    """
    GIVEN multiple mixins and mocked importlib
    WHEN get is called with the mixins
    THEN the attribute is retrieved from the imported module.
    """
    mock_import_module = mock.MagicMock()
    mixin_class_1 = type("Mixin1", (), {})
    mixin_class_2 = type("Mixin2", (), {})
    mock_import_module.return_value.Mixin1 = mixin_class_1
    mock_import_module.return_value.Mixin2 = mixin_class_2
    monkeypatch.setattr(importlib, "import_module", mock_import_module)
    mixin_values = ["module1.Mixin1", "module2.Mixin2"]

    returned_mixin_classes = mixins.get(mixins=mixin_values)

    assert returned_mixin_classes == (mixin_class_1, mixin_class_2)
    assert mock_import_module.call_count == 2
    mock_import_module.assert_any_call("module1")
    mock_import_module.assert_any_call("module2")
