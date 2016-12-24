#!/usr/bin/env python3

from setuptools import setup

import glob

setup(
    name = 'tooncher',
    packages = ['tooncher'],
    version = '0.2.0',
    description = "automates toontown rewritten's login process",
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://github.com/fphammerle/tooncher',
    download_url = 'https://github.com/fphammerle/tooncher/tarball/0.2.0',
    keywords = ['game', 'launcher', 'toontown rewritten', 'ttr'],
    classifiers = [],
    scripts = glob.glob('scripts/*'),
    install_requires = ['pyyaml'],
    tests_require = ['pytest'],
    )
