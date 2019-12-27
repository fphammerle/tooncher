import datetime
import json
import os
import pathlib
import ssl
import subprocess
import sys
import typing
import urllib.parse
import urllib.request

# official api documentation:
# https://github.com/ToontownRewritten/api-doc/blob/master/login.md
# https://github.com/ToontownRewritten/api-doc/blob/master/invasions.md

_LOGIN_API_URL = "https://www.toontownrewritten.com/api/login?format=json"


def start_engine(
    engine_path: pathlib.Path, gameserver: str, playcookie: str, **popen_kwargs
) -> subprocess.Popen:
    # without XAUTHORITY:
    # > :display:x11display(error): Could not open display ":0.0".
    # > :ToonBase: Default graphics pipe is glxGraphicsPipe (OpenGL).
    # > :ToonBase(warning): Unable to open 'onscreen' window.
    # > Traceback (most recent call last):
    # >   File "<compiled '__voltorbmain__'>", line 0, in <module>
    # >   [...]
    # >   File "<compiled 'direct.vlt8f63e471.ShowBase'>", line 0, in vltf05fd21b
    # > Exception: Could not open window.
    # optirun sets plenty of env vars
    env = os.environ.copy()
    env["TTR_GAMESERVER"] = gameserver
    env["TTR_PLAYCOOKIE"] = playcookie
    engine_path = engine_path.resolve()
    if sys.platform == "darwin":
        env["DYLD_LIBRARY_PATH"] = str(engine_path.parent.joinpath("Libraries.bundle"))
        env["DYLD_FRAMEWORK_PATH"] = str(engine_path.parent.joinpath("Frameworks"))
    return subprocess.Popen(
        args=[str(engine_path)], cwd=engine_path.parent, env=env, **popen_kwargs,
    )


def _api_request(
    url: str, params: typing.Optional[dict] = None, validate_ssl_cert: bool = True
):
    resp = urllib.request.urlopen(
        url=url,
        data=urllib.parse.urlencode(params).encode("ascii") if params else None,
        context=None if validate_ssl_cert else ssl._create_unverified_context(),
    )
    return json.loads(resp.read().decode("ascii"))


class _LoginSuccessful:
    def __init__(self, playcookie: str, gameserver: str):
        self.playcookie = playcookie
        self.gameserver = gameserver


class _LoginDelayed:
    def __init__(self, queue_token: str):
        self.queue_token = queue_token


def _login(
    username: typing.Optional[str] = None,
    password: typing.Optional[str] = None,
    queue_token: typing.Optional[str] = None,
    validate_ssl_cert: bool = True,
) -> typing.Union[_LoginSuccessful, _LoginDelayed]:
    if username is not None and queue_token is None:
        assert password is not None
        req_params = {
            "username": username,
            "password": password,
        }
    elif username is None and queue_token is not None:
        req_params = {
            "queueToken": queue_token,
        }
    else:
        raise Exception("either specify username or queue token")
    resp_data = _api_request(
        url=_LOGIN_API_URL, params=req_params, validate_ssl_cert=validate_ssl_cert,
    )
    if resp_data["success"] == "true":
        return _LoginSuccessful(
            playcookie=resp_data["cookie"], gameserver=resp_data["gameserver"],
        )
    if resp_data["success"] == "delayed":
        return _LoginDelayed(queue_token=resp_data["queueToken"],)
    raise Exception(repr(resp_data))


def launch(
    engine_path: pathlib.Path,
    username: str,
    password: str,
    validate_ssl_certs: bool = True,
    cpu_limit_percent: typing.Optional[int] = None,
) -> None:
    result = _login(
        username=username, password=password, validate_ssl_cert=validate_ssl_certs,
    )
    if isinstance(result, _LoginDelayed):
        result = _login(
            queue_token=result.queue_token, validate_ssl_cert=validate_ssl_certs,
        )
    if not isinstance(result, _LoginSuccessful):
        raise Exception("unexpected response: {!r}".format(result))
    process = start_engine(
        engine_path=engine_path,
        gameserver=result.gameserver,
        playcookie=result.playcookie,
    )
    if cpu_limit_percent is not None:
        subprocess.Popen(
            args=[
                "cpulimit",
                "--pid",
                str(process.pid),
                "--limit",
                str(cpu_limit_percent),
                # '--verbose',
            ]
        )
    process.wait()
