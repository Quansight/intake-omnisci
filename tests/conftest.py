import pytest
import yaml
from pathlib import Path
import intake

CATALOG_PATH = str(Path(__file__).parent.parent.joinpath('examples', 'omnisci-demos.yml'))  # noqa E501
CATALOG_PATH_SQL = str(Path(__file__).parent.parent.joinpath('examples', 'catalog.yml'))  # noqa E501


# @pytest.fixture
# def omnisci_cat_dict():
#     with open(CATALOG_PATH, 'r') as stream:
#         try:
#             cat = yaml.safe_load(stream)
#         except yaml.YAMLError as exc:
#             print(exc)
#
#     return cat
#
#
# @pytest.fixture
# def omnisci_sources(omnisci_cat_dict):
#     return omnisci_cat_dict['sources']


@pytest.fixture
def omnisci_cat():
    catalog = intake.open_catalog(CATALOG_PATH)
    return catalog


@pytest.fixture
def sql_cat():
    catalog = intake.open_catalog(CATALOG_PATH_SQL)
    return catalog
