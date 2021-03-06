#!/usr/bin/env python

"""
ep-tools
--------

Tools used in the organization of EuroPython.
"""

from __future__ import print_function

import os.path as op
import io
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# long description
def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# Get version without importing, which avoids dependency issues
MODULE_NAME = find_packages(exclude=["tests"])[0]
VERSION_PYFILE = op.join(MODULE_NAME, "version.py")
# set __version__ variable
exec(compile(read(VERSION_PYFILE), VERSION_PYFILE, "exec"))

# noinspection PyUnresolvedReferences
setup_dict = dict(
    name=MODULE_NAME,
    version=__version__,
    description="Tools used in the organization of EuroPython.",
    url="https://github.com/EuroPython/ep-tools",
    license="MIT License",
    author="",
    author_email="",
    maintainer="",
    maintainer_email="",
    packages=find_packages(),
    install_requires=["pandas"],
    scripts=[],
    long_description=read("README.md"),
    platforms="Linux/MacOSX",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Beta",
        "Natural Language :: English",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    extras_require={"testing": ["pytest", "pytest-cov"]},
)


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup_dict.update(dict(tests_require=["pytest"], cmdclass={"test": PyTest}))


if __name__ == "__main__":
    setup(**setup_dict)
