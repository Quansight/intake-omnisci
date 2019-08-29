#!/usr/bin/env python

from setuptools import setup, find_packages

requires = open("requirements.txt").read().strip().split("\n")

for line in open("intake_omnisci/__init__.py").readlines():
    if line.startswith("__version__") and "=" in line:
        version = line.split("=", 1)[1].split()[0].strip("'\"\t\n ")
        break
else:
    version = "0.1.0"

setup(
    name="intake-omnisci",
    version=version,
    description="OmniSci plugin for Intake",
    url="https://github.com/Quansight/intake-omnisci",
    maintainer="Pearu Peterson and Ian Rose",
    maintainer_email="pearu.peterson@quansight.com",
    license="Apache 2.0",
    py_modules=["intake_omnisci"],
    packages=find_packages(),
    package_data={"": ["*.csv", "*.yml", "*.html"]},
    include_package_data=True,
    entry_points={
        "intake.drivers": [
            "omnisci = intake_omnisci:OmniSciSource",
            "omnisci_cat = intake_omnisci:OmniSciCatalog",
        ]
    },
    install_requires=requires,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
