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
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["tooncher = tooncher._cli:main"]},
    install_requires=["pyyaml"],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest"],
)
