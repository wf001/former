import sys
from unittest import mock

import pytest

from former import __prog__
from former.__main__ import main

from .fixtures import JSON_FILE_PATH, YAML_FILE_PATH


@pytest.mark.parametrize(
    "argv",
    [
        [__prog__, "json", "yaml", "-i", JSON_FILE_PATH],
        [__prog__, "yaml", "json", "-i", YAML_FILE_PATH],
        [__prog__, "json", "yaml", "-i", JSON_FILE_PATH, "-o", YAML_FILE_PATH],
    ],
)
def test_cli_valid_args(mocker, capfd, argv):
    with mock.patch.object(sys, "argv", argv):
        mocker.patch("former.core.Former._write_file")
        r = main()
        assert r == 0


@pytest.mark.parametrize(
    "args",
    [
        [__prog__, "json"],
        [__prog__, "json", "yaml"],
        [__prog__, "json", "-i", "test.json"],
    ],
)
def test_cli_invalid_args1(capfd, args):
    with pytest.raises(SystemExit):
        with mock.patch.object(sys, "argv", args):
            main()
    out, err = capfd.readouterr()
    assert "required:" in err
    assert "error:" in err


@pytest.mark.parametrize("args", [[__prog__, "json", "yaml", "-i"]])
def test_cli_invalid_args2(capfd, args):
    with pytest.raises(SystemExit):
        with mock.patch.object(sys, "argv", args):
            main()
    out, err = capfd.readouterr()
    assert "expected one argument" in err
    assert "error:" in err


def test_cli_print_version(capfd):
    argv = [__prog__, "--v"]
    with pytest.raises(SystemExit):
        with mock.patch.object(sys, "argv", argv):
            main()
    out, err = capfd.readouterr()
    assert "version" in out


def test_cli_print_help(capfd):
    argv = [__prog__, "--h"]
    with pytest.raises(SystemExit):
        with mock.patch.object(sys, "argv", argv):
            main()
    out, err = capfd.readouterr()
    assert "usage:" in out


def test_cli_no_arg(capfd):
    argv = [__prog__]
    with pytest.raises(SystemExit):
        with mock.patch.object(sys, "argv", argv):
            main()
    out, err = capfd.readouterr()
    assert "usage:" in err
    assert "error:" in err
