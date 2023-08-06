#!/usr/bin/env python

import os.path
from io import open  # Remove this import when dropping Python 2 support
from setuptools import setup, find_packages

with open("README.md", 'r', encoding="utf8") as f:
    long_description = f.read()


def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "PySquashfsImage/__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name='PySquashfsImage',
    version=get_version(),
    description='Squashfs image parser',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Matteo Mattei; Nicola Ponzeveroni;',
    author_email='info@matteomattei.com',
    url='https://github.com/matteomattei/PySquashfsImage',
    packages=find_packages(),
    keywords=["filesystem", "parser", "squash", "squashfs"],
    python_requires=">=2.7, !=3.0.*",
    install_requires=[
        "argparse;python_version == '3.1'",
        "enum34;python_version < '3.4'",
        "python-dateutil;python_version < '3.6'"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "pysquashfs = PySquashfsImage.__main__:main",
        ]
    }
)
