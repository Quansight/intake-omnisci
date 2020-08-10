#!/usr/bin/env python

from setuptools import setup, find_packages

for line in open("intake_omnisci/__init__.py").readlines():
    if line.startswith("__version__") and "=" in line:
        version = '0.0.1'
        break
else:
    version = "0.0.1"

setup(
    name="intake-omnisci",
    version = '0.0.1'
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
            "omnisci = intake_omnisci.source:OmniSciSource",
            "omnisci_cat = intake_omnisci.catalog:OmniSciCatalog",
        ]
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
