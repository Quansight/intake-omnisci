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

See examples of how to use the driver in these notebooks:  
[01_Intake_OmniSci_example](./examples/01_Intake_OmniSci_example.ipynb)  
[02_Catalog_of_OmniSci_Demos](./examples/02_Catalog_of_OmniSci_Demos.ipynb)  

Development Environment
-----------------------

Create development Python environment:  
 `conda env create -f environment.yml`  
 
  > Note: For a faster solve, you can install mamba and use `mamba env create -f environment.yml`
 
Verify development environment by running the tests with `pytest`
 
