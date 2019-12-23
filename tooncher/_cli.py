import argparse
import os
import pathlib
import sys

import yaml

import tooncher

if sys.platform == "darwin":
    _TOONTOWN_ENGINE_DEFAULT_PATH = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "Toontown Rewritten",
        "Toontown Rewritten",
    )
else:
    _TOONTOWN_ENGINE_DEFAULT_PATH = None


def run(
    username,
    config_path,
    engine_path=None,
    validate_ssl_certs=True,
    cpu_limit_percent=None,
):
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            config = yaml.safe_load(config_file.read())
    else:
        config = {}
    if engine_path is None:
        if "engine_path" in config:
            engine_path = config["engine_path"]
        else:
            engine_path = _TOONTOWN_ENGINE_DEFAULT_PATH
    if engine_path is None:
        raise ValueError(
            "missing path to toontown engine\n"
            + "pass --engine-path, set $TOONCHER_ENGINE_PATH, or add to config file"
        )
    accounts = [a for a in config.get("accounts", []) if a["username"] == username]
    if not accounts:
        raise ValueError("username {!r} was not found in config file".format(username))
    if len(accounts) > 1:
        raise ValueError(
            "multiple entries for username {!r} in config file".format(username)
        )
    tooncher.launch(
        engine_path=pathlib.Path(engine_path),
        username=accounts[0]["username"],
        password=accounts[0]["password"],
        validate_ssl_certs=validate_ssl_certs,
        cpu_limit_percent=cpu_limit_percent,
    )


class _EnvDefaultArgparser(argparse.ArgumentParser):
    def add_argument(self, *args, envvar=None, **kwargs):
        if envvar:
            envvar_value = os.environ.get(envvar, None)
            if envvar_value:
                kwargs["required"] = False
                kwargs["default"] = envvar_value
        super().add_argument(*args, **kwargs)


def _init_argparser():
    argparser = _EnvDefaultArgparser(description=None)
    argparser.add_argument("username")
    argparser.add_argument(
        "--config",
        "-c",
        metavar="path",
        dest="config_path",
        help="path to config file (default: %(default)s)",
        default=os.path.join(os.path.expanduser("~"), ".tooncher"),
    )
    argparser.add_argument(
        "--engine-path",
        "-e",
        metavar="path",
        dest="engine_path",
        envvar="TOONCHER_ENGINE_PATH",
        default=None,
        help="path to toontown engine (overrides path in config file, "
        + "may also be set via env var $TOONCHER_ENGINE_PATH)",
    )
    argparser.add_argument(
        "--no-ssl-cert-validation",
        "-k",
        dest="validate_ssl_certs",
        help="do not validate ssl certificates",
        action="store_false",
    )
    argparser.add_argument(
        "--cpu-limit",
        dest="cpu_limit_percent",
        type=int,
        default=None,
        help="maximally allowed cpu usage in percent"
        + " (requires cpulimit command, default: %(default)s)",
    )
    return argparser


def main() -> None:
    argparser = _init_argparser()
    args = argparser.parse_args()
    run(**vars(args))
