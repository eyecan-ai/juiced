#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()

setup(
    author="Luca Bonfiglioli",
    author_email="Luca.Bonfiglioli@eyecan.ai",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="QML GUI for Pipelime",
    entry_points={
        "console_scripts": [
            "juiced=juiced.cli:main",
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="juiced",
    name="juiced",
    packages=find_packages(include=["juiced", "juiced.*"]),
    test_suite="tests",
    url="https://github.com/eyecan-ai/juiced",
    version="0.0.0",
    zip_safe=False,
)
