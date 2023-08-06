# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib
import sys
from collections.abc import Callable
from types import ModuleType

import pytest
from pytest_mock import MockerFixture


def basic(mod: ModuleType):
    assert mod.__name__ == "libdnf5"
    base = mod.base.Base()
    base.load_config_from_file()
    base.get_config()
    base.setup()


def basic_libdnf5_cli(mod: ModuleType):
    assert mod.__name__ == "libdnf5_cli"
    mod.progressbar.DownloadProgressBar(500, "abcdefgh")


PARAM = pytest.mark.parametrize(
    "module_name,checker,init",
    [
        pytest.param("libdnf5", basic, "_libdnf5_shim.initialize", id="libdnf5"),
        pytest.param(
            "libdnf5_cli",
            basic_libdnf5_cli,
            "_libdnf5_shim.initialize_cli",
            id="libdnf5_cli",
        ),
    ],
)


@PARAM
def test_libdnf5_import(
    mocker: MockerFixture,
    module_name: str,
    checker: Callable[[ModuleType], None],
    init: str,
):
    import _libdnf5_shim._impl

    initializes = mocker.spy(_libdnf5_shim._impl, "initialize")

    # Import libdnf5 for the first time
    mod = importlib.import_module(module_name)

    # Check that the shim was used
    initializes.assert_called_once()
    assert module_name in sys.modules
    assert init in sys.modules

    # Run basic tests to make sure the imported libdnf5 works
    checker(mod)

    # Import again
    mod = importlib.import_module(module_name)

    checker(mod)

    # Ensure that initialize was only called once
    initializes.assert_called_once()


@PARAM
def test_libdnf5_import_fail(
    mocker: MockerFixture,
    module_name: str,
    checker: Callable[[ModuleType], None],
    init: str,
):
    import _libdnf5_shim._impl

    initializes = mocker.spy(_libdnf5_shim._impl, "initialize")

    # Set the INTERPRETERS to an empty tuple to cause a failure
    inters = _libdnf5_shim._impl.INTERPRETERS
    _libdnf5_shim._impl.INTERPRETERS = ()

    # Check failure
    try:
        with pytest.raises(
            ImportError, match=_libdnf5_shim._impl.FAILURE_MSG.format(module_name)
        ):
            importlib.import_module(module_name)
    finally:
        _libdnf5_shim._impl.INTERPRETERS = inters

    # Check that shim was used
    initializes.assert_called_once()

    # Try to import libdnf5
    mod = importlib.import_module(module_name)  # noqa: F811

    # Check that it works now
    checker(mod)
    assert initializes.call_count == 2


def test_both_import():
    import libdnf5
    import libdnf5_cli

    basic(libdnf5)
    basic_libdnf5_cli(libdnf5_cli)
