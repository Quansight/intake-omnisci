from intake.catalog.base import Catalog
from intake.catalog.local import LocalCatalogEntry
import pymapd

from . import __version__


class OmniSciCatalog(Catalog):
    """
    Makes data sources out of known tables in the given OmniSci database.
    """

    name = "omnisci_cat"
    container = "catalog"
    version = __version__

    def __init__(
        self,
        uri=None,
        user=None,
        password=None,
        host=None,
        port=6274,
        dbname=None,
        protocol="binary",
        metadata=None,
        **kwargs,
    ):
        """
        Load data from an OmniSci database.
        Can take *either* a SQLAlchemy-compliant connection string,
        or a set uf user, password, host, port, dbname.

        Parameters:
            uri: str
                a valid OmniSci uri in the form 'mapd://user:password@host:port/database'.
            user: str
                The user name.
            password: str
                The user password.
            host: str
                The hostname for the database server.
            port: int
                The port for the database server.
            dbname: str
                The name of the database to connect to.
            protocol: str
                The protocol for the database server.
            metadata: dict
                The metadata for the source.
        """
        self._init_args = {
            "uri": uri,
            "user": user,
            "host": host,
            "password": password,
            "dbname": dbname,
            "protocol": protocol,
        }
        # Only include these if they differ from the default values.
        if protocol != "binary":
            self._init_args["protocol"] = protocol
        if port != 6274:
            self._init_args["port"] = port

        super(OmniSciCatalog, self).__init__(**kwargs)

    def _load(self):
        """
        Connect to the OmniSci database, list the available tables, and
        construct a catalog entry for each table.
        """
        connection = pymapd.connect(**self._init_args)
        self._entries = {}
        for table in connection.get_tables():
            description = "SQL table %s from %s" % (table, str(self))
            args = {key: value for key, value in self._init_args.items() if value}
            args["sql_expr"] = table
            e = LocalCatalogEntry(table, description, "omnisci", True, args)
            self._entries[table] = e
