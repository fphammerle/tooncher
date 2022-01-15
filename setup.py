import pathlib

import setuptools

setuptools.setup(
    name="tooncher",
    use_scm_version=True,
    packages=setuptools.find_packages(),
    description="automates toontown rewritten's login process",
    long_description=pathlib.Path(__file__).parent.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Fabian Peter Hammerle",
    author_email="fabian.hammerle@gmail.com",
    url="https://github.com/fphammerle/tooncher",
    keywords=["game", "launcher", "toontown rewritten", "ttr"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        # .github/workflows/python.yml
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["tooncher = tooncher._cli:main"]},
    # >=3.6 for f-strings, var type hints & enforcing kwargs with *
    # >=3.7 for dataclasses
    python_requires=">=3.7",
    # pipeline tests againsts pyyaml<5.4
    install_requires=["pyyaml<6"],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest"],
)
