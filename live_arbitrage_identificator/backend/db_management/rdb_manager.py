import logging
from enum import Enum
from pathlib import Path
from typing import Any, Set, Tuple, Type

from live_arbitrage_identificator.backend.db_management.rdb_schema_builder import RDBArbitrageSchemaBuilder
from live_arbitrage_identificator.backend.db_management.rdb_connection_wrapper import RDBConnectionWrapper
from live_arbitrage_identificator.backend.db_management.base_rdb_query_executor import BaseRDBQueryExecutor
from live_arbitrage_identificator.utils.logger import Logger

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import ThreadedConnectionPool
from pydantic import BaseModel


logger = Logger(
    log_dir="logs/database_manager",
    log_file="database_manager.log",
    log_level=logging.INFO,
)



class RDBManager(BaseRDBQueryExecutor):
    """
    Manages interactions with an RDB, providing methods for executing queries,
    managing transactions, and handling database operations.

    RDBManager implements the abstract methods from RDBQueryExecutor, providing concrete implementations
    for query execution. It serves as the primary interface for performing database operations and can
    be extended or customized as needed.

    When initialized the schema_builder is used to ensure that the database schema is up-to-date.

    Example Usage:
        db_manager = RDBManager(connection, schema_builder)
        result = db_manager.execute_query(query, params, fetch=True)

    Attributes:
        connection (RDBConnectionWrapper): A connection wrapper to interact with the database.
        schema_builder (RDBArbitrageSchemaBuilder): An instance responsible for managing the schema of the database.
    """

    def __init__(self, connection_wrapper: RDBConnectionWrapper, schema_builder: RDBArbitrageSchemaBuilder):
        """
        Args:
            connection_wrapper: A connection wrapper to interact with the database.
            schema_builder:  An instance responsible for managing the schema of the database.
        """
        super().__init__(connection_wrapper, schema_builder)
        self.schema_builder.build_schema(query_executor=self)

    def set_search_path(self, cursor: RealDictCursor, search_path: str):
        """
        Sets the search path for the given cursor.

        Args:
            cursor: The cursor to set the search path for.
            search_path: The search path to set.
        """
        cursor.execute(f"SET search_path TO {search_path};")

    def set_schema_search_path(self, cursor: RealDictCursor):
        """
        Sets the search path for the given cursor to the schema search path.

        Args:
            cursor: The cursor to set the search path for.
        """
        self.set_search_path(cursor, self.connection_wrapper.config.SCHEMA)


    def execute_query(self, query: sql.SQL, params: Tuple[Any, ...] = None, fetch: bool = False) -> Any:
        """
        Executes a query and, if necessary, fetches the results.

        Args:
            query (sql.SQL): A SQL query object.
            params (Tuple[Any, ...]): A tuple containing the values for the placeholders in the query.
            fetch (bool): Whether to fetch the results (True) or just execute the query (False).

        Returns:
            result (Any): The fetched results, if fetch is True. Otherwise, None.
        """
        with self.connection_wrapper as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                self.set_schema_search_path(cursor)
                try:
                    cursor.execute(query, params)
                except psycopg2.errors.UndefinedTable as e:
                    # TODO: Just log this, and return None
                    # Also maybe own method to handle this...
                    raise e
                except psycopg2.errors.UndefinedColumn as e:
                    # TODO: Just log this, and return None
                    # raise Exception("Column does not exist", e)
                    return None

                if fetch:
                    result = cursor.fetchall()
                else:
                    result = None
            conn.commit()

        return result

    def execute_values_query(self, query: sql.SQL, data: list[Tuple[Any, ...]]) -> None:
        """
        Executes a bulk insert/update query with a list of tuples as data.

        Args:
            query (sql.SQL): A SQL query object.
            data (List[Tuple[Any, ...]]): A list of tuples containing the values to be inserted or updated.
        """
        with self.connection_wrapper as conn:
            with conn.cursor() as cursor:
                self.set_schema_search_path(cursor)
                try:
                    execute_values(cursor, query, data)
                except psycopg2.errors.UndefinedTable as e:
                    raise Exception("Table does not exist", e)
                except psycopg2.errors.UndefinedColumn as e:
                    # TODO: Just log this, and return None
                    # raise Exception("Column does not exist", e)
                    return None
                except psycopg2.errors.InvalidColumnReference as e:
                    raise Exception(f"This query: {query}, raised: ", e)
                conn.commit()

    def run_a_script_file(self, file_path: Path) -> None:
        with open(file_path, "r") as f:
            query = f.read()
        self.execute_query(query)
