import pathlib
import shutil
import subprocess
import unittest.mock

import tooncher


def test_start_engine():
    process = tooncher.start_engine(
        engine_path=pathlib.Path(shutil.which("printenv")),
        gameserver="gameserver",
        playcookie="cookie",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert isinstance(process, subprocess.Popen)
    stdout, stderr = process.communicate()
    assert not stderr
    env = stdout.strip().split(b"\n")
    assert b"TTR_GAMESERVER=gameserver" in env
    assert b"TTR_PLAYCOOKIE=cookie" in env


@unittest.mock.patch("os.environ", {"SOME": "VAR", "OTHER": "VALUE"})
def test_start_engine_mac():
    app_support_path = "/Users/me/Library/Application Support"
    engine_path = pathlib.Path(app_support_path).joinpath(
        "Toontown Rewritten", "Toontown Rewritten"
    )
    with unittest.mock.patch("subprocess.Popen") as popen_mock:
        with unittest.mock.patch("sys.platform", "darwin"):
            # python3.5's pathlib.Path.resolve raises FileNotFoundError
            with unittest.mock.patch(
                "pathlib.Path.resolve", new=lambda p: p.with_suffix(".resolved"),
            ):
                tooncher.start_engine(
                    engine_path=engine_path,
                    gameserver="gameserver",
                    playcookie="cookie",
                    check=True,
                )
    popen_mock.assert_called_once_with(
        args=[str(engine_path) + ".resolved"],
        check=True,
        cwd=str(engine_path.parent),
        env={
            "SOME": "VAR",
            "OTHER": "VALUE",
            "TTR_GAMESERVER": "gameserver",
            "TTR_PLAYCOOKIE": "cookie",
            "DYLD_LIBRARY_PATH": app_support_path
            + "/Toontown Rewritten/Libraries.bundle",
            "DYLD_FRAMEWORK_PATH": app_support_path + "/Toontown Rewritten/Frameworks",
        },
    )


def test_start_engine_xorg():
    with unittest.mock.patch("subprocess.Popen") as popen_mock:
        with unittest.mock.patch("os.environ", {"XAUTHORITY": "/home/me/.Xauthority"}):
            with unittest.mock.patch("sys.platform", "linux"):
                with unittest.mock.patch(  # python3.5
                    "pathlib.Path.resolve", new=lambda p: p.with_suffix(".resolved"),
                ):
                    tooncher.start_engine(
                        engine_path=pathlib.PosixPath(
                            "/opt/toontown-rewritter/TTREngine"
                        ),
                        gameserver="gameserver.tld",
                        playcookie="cookie123",
                        check=False,
                    )
    popen_mock.assert_called_once_with(
        args=["/opt/toontown-rewritter/TTREngine.resolved"],
        check=False,
        cwd="/opt/toontown-rewritter",
        env={
            "TTR_GAMESERVER": "gameserver.tld",
            "TTR_PLAYCOOKIE": "cookie123",
            "XAUTHORITY": "/home/me/.Xauthority",
        },
    )
