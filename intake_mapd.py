__version__ = '0.1'

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse  # Python 2.x

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
        super(MapDDBSource, self).__init__(container='dataframe',
                                           metadata=metadata)

        self._init_args = {
            'uri': uri,
            'collection': collection,
            'projection': projection,
        }

        scheme_name = 'mapd'
        try:
            split_url = urlparse.urlsplit(uri, scheme=scheme_name)
            # perform some checking...
            path = urlparse.unquote(split_url.path).split('/')

            if (split_url.scheme != scheme_name or
                    split_url.hostname is None or
                    split_url.port is None or
                    len(path) != 2 or path[0] != '' or
                    split_url.query != '' or
                    split_url.fragment != ''):
                raise Exception()
        except Exception as e:
            new_e = Exception('Unsupported URI for a {name} source: {uri}. Use {scheme}://host:port/database'\
                              .format(name=type (self).__name__,
                                      scheme=scheme_name,
                                      uri = uri
                              ))
            new_e.original = e
            raise new_e

        self._uri = uri
        self._host = split_url.hostname
        self._port = int(split_url.port)
        self._database = path[1]  # the path portion pointing to the database
        self._collection = collection
        self._projection = projection
        self._dtypes = None
        self._adapter = None

    def _make_adapter(self):
        # TODO: use pymapd to initialize _adapter
        #self._adapter = ...
        raise NotImplementedError ('{}._make_adapter'.format(type(self).__name__))
        
    def _get_schema(self):
        if self._adapter is None:
            self._make_adapter()

        if self._dtypes is None:
            # TODO: use pymapd to get dtypes
            self._dtypes = pandas.DataFrame(
                self._adapter[self._projection][0:10]).dtypes
            
        return intake.source.base.Schema(
            datashape='datashape',
            dtype=self._dtypes,
            shape=(None, len(self._dtypes)),
            npartitions=2,
            extra_metadata={}
        )

    def _get_partition(self, _):
        return pandas.DataFrame(self._adapter[self._projection][:])
    

    def _close(self):
        # close any files, sockets, etc
        self._adapter = None
