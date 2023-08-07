from live_arbitrage_identificator.backend.db_management.base_rdb_schema_builder import BaseRDBSchemaBuilder
from live_arbitrage_identificator.backend.db_management.base_rdb_query_executor import BaseRDBQueryExecutor
from live_arbitrage_identificator.utils import get_current_enum_values
from typing import Type, Optional, Set
from enum import Enum
from psycopg2 import sql
from live_arbitrage_identificator.utils.path_helpers import get_abs_path_from_relative_backend
from live_arbitrage_identificator.backend.data_models.enums.game_status import GameStatus
from live_arbitrage_identificator.backend.data_models.enums.outcome_reason import OutcomeReason
from live_arbitrage_identificator.backend.data_models.enums.participant_type import ParticipantType
from live_arbitrage_identificator.backend.data_models.enums.scraper_type import ScraperType
from live_arbitrage_identificator.backend.data_models.enums.sport_types import SportType


class RDBArbitrageSchemaBuilder(BaseRDBSchemaBuilder):
    """
    Class for building the RDB schema used for the arbitrage identification system, including the base tables
    and the update of pre-filled tables to match the GameStatus enum and so forth.

    The schema is built using .sql script files and python Enum classes + countries.json file.
    This class uses the interface defined in BaseRDBSchemaBuilder, i.e., it implements build_schema method to be used
    with an implementation of BaseRDBQueryExecutor, e.g., RDBArbitrageQueryExecutor.
    """

    def __init__(self):
        self.query_executor: BaseRDBQueryExecutor = None

    def build_schema(self, query_executor: BaseRDBQueryExecutor, schema: Optional[str] = None):
        """
        Using .sql script files and python Enum classes + countries.json file we prepare the RDB Schema,
        while pre-filling necessary data, e.g., countries, sport_types, and so on and so forth.
        """
        self.query_executor = query_executor
        self._ensure_schema_exists(schema=schema)
        self._build_base_tables()
        self._update_prefill_base_tables()
        self._build_tables()

    def _ensure_schema_exists(self, schema: Optional[str] = None):
        self._raise_error_if_no_query_executor()
        if schema is None:
            schema = self.query_executor.connection_wrapper.config.SCHEMA

        self.query_executor.execute_query(f"CREATE SCHEMA IF NOT EXISTS {schema};")

    def _build_base_tables(self):
        self._raise_error_if_no_query_executor()
        script_path = get_abs_path_from_relative_backend(
            f"db_management/sql_queries/create_schema/create_base_tables.sql"
        )
        self.query_executor.run_a_script_file(script_path)

    def _update_prefill_base_tables(self):
        """
        This functions pre-fills the base tables using multiple sources.

        1. Some of the tables are one-to-one with the python Enum classes, e.g., sport_types, status_options, etc.
        2. countries table is pre-filled using countries.json file
        3.

        :return:
        """
        self._raise_error_if_no_query_executor()
        self._sync_enum_with_table(GameStatus, "status_option", "status")
        self._sync_enum_with_table(OutcomeReason, "outcome_reason", "reason")
        self._sync_enum_with_table(ParticipantType, "participant_type", "name")
        self._sync_enum_with_table(ScraperType, "scraper_type", "scraper_type")
        self._sync_enum_with_table(SportType, "sport_type", "sport_type")
        self._update_countries_table()

    def _build_tables(self):
        """Builds the tables for the RDB following the schema design so that the tables are connected properly."""
        self._build_level1_tables()
        self._build_level2_tables()
        self._build_level3_tables()
        self._build_level4_tables()

    def _build_level1_tables(self):
        script_path = get_abs_path_from_relative_backend(
            f"db_management/sql_queries/create_schema/create_level1_tables.sql"
        )
        self.query_executor.run_a_script_file(script_path)

    def _build_level2_tables(self):
        script_path = get_abs_path_from_relative_backend(
            f"db_management/sql_queries/create_schema/create_level2_tables.sql"
        )
        self.query_executor.run_a_script_file(script_path)

    def _build_level3_tables(self):
        script_path = get_abs_path_from_relative_backend(
            f"db_management/sql_queries/create_schema/create_level3_tables.sql"
        )
        self.query_executor.run_a_script_file(script_path)

    def _build_level4_tables(self):
        script_path = get_abs_path_from_relative_backend(
            f"db_management/sql_queries/create_schema/create_level4_tables.sql"
        )
        self.query_executor.run_a_script_file(script_path)

    def _update_countries_table(self):
        ...

    def _sync_enum_with_table(self, enum_class: Type[Enum], table_name: str, column_name: str) -> None:
        """Sync an enumeration table in the database with a Python Enum class.

        This method ensures that an SQL table remains consistent with a Python Enum class.
        The SQL table and Enum class are expected to have a one-to-one mapping. The SQL
        table should have a serial 'id' field as primary key and a 'status' field corresponding
        to the Enum class members.

        If a new member is added to the Enum, a new record with a unique 'id'
        and 'status' equivalent to the Enum member is added to the SQL table. If a member
        is removed from the Enum, the corresponding record is removed from the SQL table.

        Args:
            enum_class (Type[Enum]): The Python Enum class to synchronize with.
            table_name (str): The name of the SQL table to synchronize.
        """
        self._raise_error_if_no_query_executor()
        current_enum_values = get_current_enum_values(enum_class)
        current_db_values = self._get_current_db_values(table_name, column_name)
        self._add_new_enum_values_to_db(table_name, current_enum_values, current_db_values, column_name)
        self._remove_old_enum_values_from_db(table_name, current_enum_values, current_db_values, column_name)

    def _get_current_db_values(self, table_name: str, column_name: str) -> Set[str]:
        self._raise_error_if_no_query_executor()
        query = sql.SQL(f"SELECT {column_name} FROM {table_name}")
        try:
            res = set(row[{column_name}] for row in self.query_executor.execute_query(query, fetch=True))
        except TypeError:
            res = set()

        return res

    def _add_new_enum_values_to_db(
        self,
        table_name: str,
        current_enum_values: Set[str],
        current_db_values: Set[str],
        column_name: str,
    ) -> None:
        self._raise_error_if_no_query_executor()
        values_to_add = current_enum_values - current_db_values
        if values_to_add:
            query = sql.SQL(
                f"INSERT INTO {table_name} ({column_name}) VALUES %s ON CONFLICT ({column_name}) DO NOTHING"
            )
            data = [(value,) for value in values_to_add]
            self.query_executor.execute_values_query(query, data)

    def _remove_old_enum_values_from_db(
        self,
        table_name: str,
        current_enum_values: Set[str],
        current_db_values: Set[str],
        column_name: str,
    ) -> None:
        self._raise_error_if_no_query_executor()
        values_to_remove = current_db_values - current_enum_values
        if values_to_remove:
            query = sql.SQL(f"DELETE FROM {table_name} WHERE {column_name} IN %s")
            data = [(value,) for value in values_to_remove]
            self.query_executor.execute_query(query, data)
