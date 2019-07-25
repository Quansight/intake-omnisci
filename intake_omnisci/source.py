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
    name = "omnisci"
    container = "dataframe"
    partition_access = False

    def __init__(
        self,
        sql_expr,
        uri=None,
        user=None,
        password=None,
        host=None,
        port=6274,
        dbname=None,
        protocol="binary",
        metadata=None,
    ):
        """
        Load data from an OmniSci database.
        Can take *either* a SQLAlchemy-compliant connection string,
        or a set uf user, password, host, port, dbname.

        Parameters:
            sql_expr: str
                The data to query from the database. Can either be a table name
                or a SQL query.
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

        self._uri = uri
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbname = dbname
        self._protocol = protocol
        self._sql_expr = sql_expr
        self._dtypes = None
        self._connection = None

        super().__init__(metadata=metadata)

    def _make_cursor(self):
        if not self._connection:
            self._connection = pymapd.connect(
                uri=self._uri,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                protocol=self._protocol,
                dbname=self._dbname,
            )
        if self._sql_expr in self._connection.get_tables():
            expr = f"SELECT * FROM {self._sql_expr}"
        else:
            expr = self._sql_expr
        return self._connection.execute(expr)

    def _get_schema(self):
        if self._dtypes is None:
            cursor = self._make_cursor()

            # TODO: pymapd provides some data for querying column types.
            # Can we use that here? This requires an extra fetch, but
            # should work for more complex queries.
            self._dtypes = pandas.DataFrame.from_records(cursor.fetchmany(1)).dtypes
            cursor.close()

        return Schema(
            datashape="datashape",
            dtype=self._dtypes,
            shape=(None, len(self._dtypes)),
            npartitions=1,
            extra_metadata={},
        )

    def _get_partition(self, _):
        self._get_schema()
        cursor = self._make_cursor()
        columns = [d.name for d in cursor.description]
        records = cursor.fetchall()
        cursor.close()
        return pandas.DataFrame.from_records(records, columns=columns)

    def read(self):
        self._dataframe = self._get_partition(0)
        return self._dataframe

    def _close(self):
        # close any files, sockets, etc
        if self._connection:
            self._connection.close()
            self._connection = None
        self._dataframe = None
