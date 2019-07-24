#!/usr/bin/env python

from setuptools import setup

requires = open('requirements.txt').read().strip().split('\n')

for line in open('intake_omnisci.py').readlines():
    if line.startswith('__version__') and '=' in line:
        version = line.split('=', 1)[1].split()[0].strip ('\'"\t\n ')
        break
else:
    version = '0.0.1'

setup(
    name='intake-omnisci',
    version=version,
    description='MapD plugin for Intake',
    url='https://github.com/Quansight/intake-omnisci',
    maintainer='Pearu Peterson',
    maintainer_email='pearu.peterson@quansight.com',
    #license='BSD',
    py_modules=['intake_omnisci'],
    package_data={'': ['*.csv', '*.yml', '*.html']},
    include_package_data=True,
    install_requires=requires,
    long_description=open('README.md').read(),
    zip_safe=False,
)
