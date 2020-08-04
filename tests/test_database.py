import yaml
import ibis
from ibis.omniscidb.client import OmniSciDBClient


def db_connect(omnisci_cat, table):
    """helper function to connect to databases in the catalog"""
    cat_entry = omnisci_cat[table].describe()['args']
    omnisci_client = ibis.omniscidb.connect(
        user=cat_entry['user'],
        password=cat_entry['password'],
        host=cat_entry['host'],
        port=cat_entry['port'],
        database=cat_entry['dbname'],
        protocol=cat_entry['protocol']
    )
    return omnisci_client


def db_connect_uri(sql_cat, table):
    """helper function to connect to databases in the catalog"""
    # get uri from catalog object
    # uri = sql_cat[table]._ibis_con.uri
    uri = sql_cat[table].describe()['args']['uri']
    omnisci_client = ibis.omniscidb.connect(
        uri=uri
    )
    return omnisci_client
    

def test_db_connection_ships(omnisci_cat):
    """test the connection to the ships db"""
    omnisci_client = db_connect(omnisci_cat, 'ships')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()


def test_db_connection_flights(omnisci_cat):
    """test the connection to the flights db"""
    omnisci_client = db_connect(omnisci_cat, 'flights')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()
    

def test_db_connection_census(omnisci_cat):
    """test the connection to the census db"""
    omnisci_client = db_connect(omnisci_cat, 'census')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()
    
    
def test_db_connection_political(omnisci_cat):
    """test the connection to the political db"""
    omnisci_client = db_connect(omnisci_cat, 'political')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()

    
def test_db_connection_metis(omnisci_cat):
    """test the connection to the metis db"""
    omnisci_client = db_connect(omnisci_cat, 'metis')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()


def test_db_connection_flights_uri(sql_cat):
    """test the connection to the flights db"""
    omnisci_client = db_connect_uri(sql_cat, 'flights')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()


def test_db_connection_faults_uri(sql_cat):
    """test the connection to the flights db"""
    omnisci_client = db_connect_uri(sql_cat, 'faults')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()


def test_db_connection_metis_uri(sql_cat):
    """test the connection to the flights db"""
    omnisci_client = db_connect_uri(sql_cat, 'metis')
    assert isinstance(omnisci_client, OmniSciDBClient)
    omnisci_client.close()

