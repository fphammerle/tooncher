import subprocess


def test_cli_help():
    proc_info = subprocess.run(
        ["tooncher", "--help"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert b"optional arguments:" in proc_info.stdout
    assert not proc_info.stderr
