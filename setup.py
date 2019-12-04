import glob

import setuptools

setuptools.setup(
    name="tooncher",
    use_scm_version=True,
    packages=["tooncher"],
    description="automates toontown rewritten's login process",
    author="Fabian Peter Hammerle",
    author_email="fabian.hammerle@gmail.com",
    url="https://github.com/fphammerle/tooncher",
    download_url="https://github.com/fphammerle/tooncher/tarball/0.3.1",
    keywords=["game", "launcher", "toontown rewritten", "ttr"],
    classifiers=[],
    scripts=glob.glob("scripts/*"),
    install_requires=["pyyaml"],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest"],
)
