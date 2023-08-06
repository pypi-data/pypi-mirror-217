#!/usr/bin/env python3
import os
import pathlib
import shutil

from setuptools import Command
from setuptools import setup

NAME = "pop_loop"
DESC = "Plugins that allow alternate io loops to be used to run asynchronous code in pop projects"

# Version info -- read without importing
_locals = {}
with pathlib.Path("pop_loop", "version.py").open() as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals["version"]
SETUP_DIRNAME = pathlib.Path(__file__).parent
if not SETUP_DIRNAME:
    SETUP_DIRNAME = pathlib.Path.cwd()

with open("README.rst", encoding="utf-8") as f:
    LONG_DESC = f.read()

with pathlib.Path("requirements", "base.txt").open() as f:
    REQUIREMENTS = f.read().splitlines()

REQUIREMENTS_EXTRA = {"full": set()}
EXTRA_PATH = pathlib.Path("requirements", "extra")
for extra in EXTRA_PATH.iterdir():
    with extra.open("r") as f:
        REQUIREMENTS_EXTRA[extra.stem] = f.read().splitlines()
        REQUIREMENTS_EXTRA["full"].update(REQUIREMENTS_EXTRA[extra.stem])


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (NAME, "tests"):
            for root, dirs, files in os.walk(
                os.path.join(os.path.dirname(__file__), subdir)
            ):
                for dir_ in dirs:
                    if dir_ == "__pycache__":
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in (NAME,):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, ".")
            modules.append(modname)
    return modules


setup(
    name="pop-loop",
    author="VMware, Inc.",
    author_email="idemproject@vmware.com",
    url="https://vmware.gitlab.io/pop/pop-loop/en/latest/index.html",
    project_urls={
        "Code": "https://gitlab.com/vmware/pop/pop-loop",
        "Issue tracker": "https://gitlab.com/vmware/pop/pop-loop/issues",
    },
    version=VERSION,
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRA,
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/x-rst",
    python_requires=">=3.8",
    license="Apache Software License 2.0",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=discover_packages(),
    cmdclass={"clean": Clean},
)
