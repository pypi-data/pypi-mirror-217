from typing import Optional

from atoti._docs_utils import EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS
from atoti._java_api import JavaApi
from atoti.directquery._external_database_connection_info import (
    ExternalDatabaseConnectionInfo,
)
from atoti_core import doc

from .connection import DatabricksConnection
from .table import DatabricksTable


class DatabricksConnectionInfo(
    ExternalDatabaseConnectionInfo[DatabricksConnection, DatabricksTable]
):
    """Information needed to connect to a Databricks database."""

    @doc(**EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
    ):
        """Create a Databricks connection info.

        Args:
            url: The JDBC connection string.
            {password}

        Example:
                >>> import os
                >>> from atoti_directquery_databricks import DatabricksConnectionInfo
                >>> connection_info = DatabricksConnectionInfo(
                ...     "jdbc:databricks://"
                ...     + os.environ["DATABRICKS_SERVER_HOSTNAME"]
                ...     + "/default;"
                ...     + "transportMode=http;"
                ...     + "ssl=1;"
                ...     + "httpPath="
                ...     + os.environ["DATABRICKS_HTTP_PATH_LATEST"]
                ...     + ";"
                ...     + "AuthMech=3;"
                ...     + "UID=token;",
                ...     password=os.environ["DATABRICKS_AUTH_TOKEN"],
                ... )

        """
        super().__init__(database_key="DATABRICKS", password=password, url=url)

    def _get_database_connection(self, java_api: JavaApi) -> DatabricksConnection:
        return DatabricksConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
