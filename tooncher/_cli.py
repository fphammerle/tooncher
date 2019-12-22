import os

import argparse
import yaml

import tooncher


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
            raise Exception("missing path to toontown engine")
    accounts = config["accounts"] if "accounts" in config else []
    for account in accounts:
        if account["username"] == username:
            tooncher.launch(
                engine_path=engine_path,
                username=account["username"],
                password=account["password"],
                validate_ssl_certs=validate_ssl_certs,
                cpu_limit_percent=cpu_limit_percent,
            )


def _init_argparser():
    argparser = argparse.ArgumentParser(description=None)
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
        default=tooncher.TOONTOWN_ENGINE_DEFAULT_PATH,
        help="\n".join(
            [
                "path to toontown engine.",
                "this overrides the one specified in config file",
                "(default: %(default)s)",
            ]
        ),
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
