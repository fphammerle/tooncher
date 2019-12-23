import pathlib
import subprocess
from unittest.mock import patch

import pytest
import yaml

# pylint: disable=protected-access
import tooncher._cli


def test_cli_help():
    proc_info = subprocess.run(
        ["tooncher", "--help"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert b"optional arguments:" in proc_info.stdout
    assert not proc_info.stderr


@patch("tooncher._cli.run")
@patch("os.environ", {})
def test_engine_path_arg(run_mock):
    with patch("sys.argv", ["", "--engine-path", "/opt/ttr/TTREngine", "username"]):
        tooncher._cli.main()
    run_mock.assert_called_once()
    args, kwargs = run_mock.call_args
    assert not args
    assert kwargs["engine_path"] == "/opt/ttr/TTREngine"


@patch("tooncher._cli.run")
@patch("os.environ", {"TOONCHER_ENGINE_PATH": "/opt/ttr/TTREnvine"})
def test_engine_path_env(run_mock):
    with patch("sys.argv", ["", "username"]):
        tooncher._cli.main()
    run_mock.assert_called_once()
    args, kwargs = run_mock.call_args
    assert not args
    assert kwargs["engine_path"] == "/opt/ttr/TTREnvine"


@patch("tooncher._cli.run")
@patch("os.environ", {"TOONCHER_ENGINE_PATH": "/opt/ttr/TTREnvine"})
def test_engine_path_arg_env(run_mock):
    with patch("sys.argv", ["", "--engine-path", "/opt/ttr/TTREngine", "username"]):
        tooncher._cli.main()
    run_mock.assert_called_once()
    args, kwargs = run_mock.call_args
    assert not args
    assert kwargs["engine_path"] == "/opt/ttr/TTREngine"


@patch("tooncher.launch")
@patch("os.environ", {})
def test_engine_path_config(launch_mock, tmpdir):
    config_file = tmpdir.join("config")
    config_file.write(
        yaml.safe_dump(
            {
                "engine_path": "/opt/conf/TTR",
                "accounts": [{"username": "someone", "password": "secret"}],
            }
        )
    )
    with patch("sys.argv", ["", "--config", config_file.strpath, "someone"]):
        tooncher._cli.main()
    launch_mock.assert_called_once()
    args, kwargs = launch_mock.call_args
    assert not args
    assert kwargs["engine_path"] == pathlib.Path("/opt/conf/TTR")


@patch("tooncher.launch")
@patch("os.environ", {"TOONCHER_ENGINE_PATH": "/opt/ttr/TTREnvine"})
def test_engine_path_env_config(launch_mock, tmpdir):
    config_file = tmpdir.join("config")
    config_file.write(
        yaml.safe_dump(
            {
                "engine_path": "/opt/conf/TTR",
                "accounts": [{"username": "someone", "password": "secret"}],
            }
        )
    )
    with patch("sys.argv", ["", "--config", config_file.strpath, "someone"]):
        tooncher._cli.main()
    launch_mock.assert_called_once()
    args, kwargs = launch_mock.call_args
    assert not args
    assert kwargs["engine_path"] == pathlib.Path("/opt/ttr/TTREnvine")


@patch("tooncher.launch")
def test_account(launch_mock, tmpdir):
    config_file = tmpdir.join("config")
    config_file.write(
        yaml.safe_dump(
            {
                "engine_path": "/opt/conf/TTR",
                "accounts": [
                    {"username": "someone", "password": "secret"},
                    {"username": "toon", "password": "town"},
                ],
            }
        )
    )
    with patch("sys.argv", ["", "--config", config_file.strpath, "toon"]):
        tooncher._cli.main()
    launch_mock.assert_called_once_with(
        engine_path=pathlib.Path("/opt/conf/TTR"),
        username="toon",
        password="town",
        validate_ssl_certs=True,
        cpu_limit_percent=None,
    )


def test_account_duplicate_username(tmpdir):
    config_file = tmpdir.join("config")
    config_file.write(
        yaml.safe_dump(
            {
                "engine_path": "/opt/conf/TTR",
                "accounts": [
                    {"username": "someone", "password": "secret"},
                    {"username": "toon", "password": "town"},
                    {"username": "toon", "password": "town2"},
                ],
            }
        )
    )
    with patch("sys.argv", ["", "--config", config_file.strpath, "toon"]):
        with pytest.raises(ValueError, match=r"multiple .* username"):
            tooncher._cli.main()


def test_account_unknown_username(tmpdir):
    config_file = tmpdir.join("config")
    config_file.write(
        yaml.safe_dump(
            {
                "engine_path": "/opt/conf/TTR",
                "accounts": [
                    {"username": "someone", "password": "secret"},
                    {"username": "toon", "password": "town"},
                ],
            }
        )
    )
    with patch("sys.argv", ["", "--config", config_file.strpath, "player"]):
        with pytest.raises(ValueError, match=r"not found"):
            tooncher._cli.main()
