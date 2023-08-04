from abc import ABC, abstractmethod
from typing import Tuple, Any, List
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from pathlib import Path

class BaseRDBQueryExecutor(ABC):
    """
    Abstract base class for executing queries against a relational database (RDB).

    This class provides a common interface for interacting with various RDB systems,
    enabling the execution of SQL queries and bulk insert/update operations.
    It forms a critical part of the database management architecture, abstracting the underlying
    interactions with the database.

    Subclasses must implement the following methods to cater to specific database needs:
    - set_search_path: Configures the search path for database queries.
    - execute_query: Executes individual SQL queries, with optional fetching of results.
    - execute_values_query: Performs bulk insert/update operations using a list of tuples.
    - run_a_script_file: Executes a SQL script file.

    By defining this interface, the class promotes flexibility and extensibility,
    allowing for an easier adaptation to different database systems and potential future enhancements.

    # Example Usage:
        class MyRDBQueryExecutor(BaseRDBQueryExecutor):
            ...

        query_executor = MyRDBQueryExecutor()
        results = query_executor.execute_query(query, params, fetch=True)

    # See Also:
        - RDBConnectionWrapper
        - RDBSchemaBuilder
        - RDBManager
    """

    @abstractmethod
    def set_search_path(self, cursor: RealDictCursor) -> None:
        """
        Sets the search path for the given cursor.

        Params:
            cursor (RealDictCursor): The cursor to set the search path for.
        """
        ...

    @abstractmethod
    def execute_query(self, query: sql.SQL, params: Tuple[Any, ...] = None, fetch: bool = False) -> Any:
        """
        Executes a query and, if necessary, fetches the results.

        Params:
            query (sql.SQL): A SQL query object.
            params (Tuple[Any, ...]): A tuple containing the values for the placeholders in the query.
            fetch (bool): Whether to fetch the results (True) or just execute the query (False).

        Returns:
            result (Any): The fetched results, if fetch is True. Otherwise, None.
        """
        ...

    @abstractmethod
    def execute_values_query(self, query: sql.SQL, data: List[Tuple[Any, ...]]) -> None:
        """
        Executes a bulk insert/update query with a list of tuples as data.

        Params:
            query (sql.SQL): A SQL query object.
            data (List[Tuple[Any, ...]]): A list of tuples containing the values to be inserted or updated.
        """
        ...

    @abstractmethod
    def run_a_script_file(self, file_path: Path) -> None:
        """
        Executes an SQL script file.

        Params:
            file_path (Path): The path to the script file.
        """
        ...