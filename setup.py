#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="intake-omnisci",
    version='0.0.1',
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
