""" Implements intake-mapd Plugin.
"""
# Author: Pearu Peterson
# Created: Apr 2018

__version__ = '0.1'

import pandas
from intake.source import base
import pymapd

class Plugin(base.Plugin):

    def __init__(self):
        super(Plugin, self).__init__(name='mapd',
                                     version=__version__,
                                     container='dataframe',
                                     partition_access=False,
        )

    def open(self, uri, collection, projection, **kwargs):
        """
        Create MapDDBSource instance

        Parameters:
            uri : str
                Full MapD URI for the database connection.
            collection : a mapd valid query
                mapd query to be executed.
            projection : a mapd valid projection
                mapd projection
            kwargs (dict):
                Additional parameters to pass as keyword arguments to
                ``??` constructor.
        """
        base_kwargs, source_kwargs = self.separate_base_kwargs(kwargs)
        return MapDDBSource(uri=uri,
                            collection=collection,
                            projection=projection,
                            metadata=base_kwargs['metadata'])


class MapDDBSource(base.DataSource):
    
    def __init__(self, uri, collection, projection, metadata=None):
        """Load data from MapD

        Parameters:
            uri: str
                a valid mongodb uri in the form '[mapd:]//host:port/database'.
            collection: str
                The collection in the database that will act as source;
            projection: tuple/list
                The fields to query.
            metadate: dict
                The metadata to keep
        """
        super(MapDDBSource, self).__init__(container='dataframe', metadata=metadata)

        self._init_args = {
            'uri': uri,
            'collection': collection,
            'projection': projection,
        }

        self._uri = uri        
        self._collection = collection
        self._projection = projection
        self._dtypes = None
        self._adapter = None

    def _make_adapter(self):
        select_cmd = 'SELECT {} FROM {}'.format(', '.join(self._projection or ['*']), self._collection)
        self._adapter = pymapd.connect(self._uri).execute(select_cmd) # Cursor
        
    def _get_schema(self):
        if self._adapter is None:
            self._make_adapter()

        if self._dtypes is None:
            # TODO: use pymapd tools to fill dtypes
            self._dtypes = pandas.DataFrame.from_records(self._adapter.fetchmany(1)).dtypes
            
        return base.Schema(
            datashape='datashape',
            dtype=self._dtypes,
            shape=(None, len(self._dtypes)),
            npartitions=2,
            extra_metadata={}
        )

    def _get_partition(self, _):
        return pandas.DataFrame.from_records(self._adapter.fetchall(), columns=self._projection)

    def _close(self):
        # close any files, sockets, etc
        if self._adapter is not None:
            self._adapter.close()
            self._adapter = None
