from abc import ABC, abstractmethod
from typing import Optional
from live_arbitrage_identificator.backend.db_management.base_rdb_query_executor import BaseRDBQueryExecutor


class BaseRDBSchemaBuilder(ABC):
    """
    Abstract base class for building and managing the schema of an RDB.

    For example, see RDBArbitrageSchemaBuilder that implements this for the PostgresSQL database schema.
    """

    def set_query_executor(self, query_executor: BaseRDBQueryExecutor):
        """
        Sets the query executor to use for executing queries.

        Args:
            query_executor (BaseRDBQueryExecutor): The query executor to use for executing the query.
        """
        self.query_executor = query_executor

    def get_query_executor(self) -> BaseRDBQueryExecutor:
        """
        Returns the query executor to use for executing queries.

        Returns:
            BaseRDBQueryExecutor: The query executor to use for executing the query.
        """
        return self.query_executor

    def _raise_error_if_no_query_executor(self):
        if self.query_executor is None:
            raise ValueError("Query executor is None. Did you forget to call build_schema?")
        elif not isinstance(self.query_executor, BaseRDBQueryExecutor):
            raise ValueError(
                f"Query executor is not of type BaseRDBQueryExecutor. Got {type(self.query_executor)}."
            )

    @abstractmethod
    def _ensure_schema_exists(self, schema: Optional[str] = None):
        """
        Ensures that the schema exists in the database.

        Args:
            query_executor (BaseRDBQueryExecutor): The query executor to use for executing the query.
            schema (str): The name of the schema to check for. If None, the default schema is checked.
        """
        ...

    @abstractmethod
    def build_schema(self, query_executor: BaseRDBQueryExecutor, schema: Optional[str] = None):
        """
        Builds the schema in the database.
        """
        ...

    @abstractmethod
    def _build_tables(self):
        """
        Builds the tables in the database.
        """
        ...

    @abstractmethod
    def _update_prefill_base_tables(self):
        """
        Updates the prefilled base tables in the database.

        Note:
            This method is only used for the initial prefilling of the database, thus
            all the schemas do not need this.
            Hence, some implementations of this method may be simple pass statements.
        """
        ...
