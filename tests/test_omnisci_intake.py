from ibis.omniscidb.client import OmniSciDBTable


def test_to_ibis(omnisci_cat):
    table = omnisci_cat.metis.uk_wells.to_ibis()
    isinstance(table, OmniSciDBTable)
