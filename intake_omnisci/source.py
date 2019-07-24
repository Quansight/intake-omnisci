""" Implements intake-omnisci driver.
"""
from intake.source.base import DataSource, Schema
import pandas
import pymapd

from . import __version__

class OmniSciSource(DataSource):
    """
    An intake data source representing data from an OmniSci database table.
    """
    version = __version__
    name = 'omnisci'
    container = 'dataframe'
    partition_access = False

    def __init__(self, uri, collection, projection=None, metadata=None):
        """Load data from OmniSci

        Parameters:
            uri: str
                a valid OmniSci uri in the form 'protocol://host:port/database'.
            collection: str
                The collection in the database that will act as a source.
                Can either be a table name or a SQL query.
            projection: tuple/list
                The fields to query.
            metadata: dict
                The metadata to keep
        """

        self._uri = uri        
        self._collection = collection
        self._projection = projection
        self._dtypes = None
        self._connection = None

        super().__init__(metadata=metadata)

    def _make_connection(self):
        select_cmd = 'SELECT {} FROM {} LIMIT 10'.format(', '.join(self._projection or ['*']), self._collection)
        self._connection = pymapd.connect(self._uri).execute(select_cmd) # Cursor
        
    def _get_schema(self):
        if self._connection is None:
            self._make_connection()

        if self._dtypes is None:
            # TODO: use pymapd tools to fill dtypes
            self._dtypes = pandas.DataFrame.from_records(self._connection.fetchmany(1)).dtypes
            
        return Schema(
            datashape='datashape',
            dtype=self._dtypes,
            shape=(None, len(self._dtypes)),
            npartitions=1,
            extra_metadata={}
        )

    def _get_partition(self, _):
        self._get_schema()
        return pandas.DataFrame.from_records(self._connection.fetchall(), columns=self._projection)

    def read(self):
        self._dataframe = self._get_partition(1)
        return self._dataframe

    def _close(self):
        # close any files, sockets, etc
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        self._dataframe = None
