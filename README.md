# intake-omnisci
An [OmniSci](https://www.omnisci.com) driver for
[intake](https://intake.readthedocs.io/en/latest).

## Installation
You can install this driver by running
```
pip install intake-omnisci
```
Intake should automatically be able to pick it up and use it when encountering
an OmniSci data source in a catalog.

## Usage

See an example of how to use the driver in
[this](./examples/example.ipynb) notebook.

Development Environment
-----------------------

 * Create development Python environment.
 * Install conda: `conda install conda=4.5`
 * Install jupyter: `conda install jupyter`
 * Install [intake](https://github.com/ContinuumIO/intake): `conda install -c intake intake`
 * `pip install -r requirements.txt`
 * `python setup.py develop`
 * Verify development environment by running the unit tests with `py.test`.
 
