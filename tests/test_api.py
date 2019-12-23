import pathlib
import shutil
import subprocess

import pytest

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
    assert b"" == stderr
    env = stdout.strip().split(b"\n")
    assert b"TTR_GAMESERVER=gameserver" in env
    assert b"TTR_PLAYCOOKIE=cookie" in env
