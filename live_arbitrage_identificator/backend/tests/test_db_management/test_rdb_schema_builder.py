import unittest
from unittest.mock import Mock, patch
from typing import Type, Optional
from enum import Enum

from live_arbitrage_identificator.backend.db_management.rdb_schema_builder import RDBArbitrageSchemaBuilder
from live_arbitrage_identificator.backend.db_management.base_rdb_query_executor import BaseRDBQueryExecutor


class TestRDBArbitrageSchemaBuilder(unittest.TestCase):
    def setUp(self):
        self.query_executor_mock = Mock(spec=BaseRDBQueryExecutor)
        self.schema_builder = RDBArbitrageSchemaBuilder()

    def test_build_schema(self):
        """
        Super simple test to ensure that build_schema executes the correct queries.
        """
        with patch.object(self.schema_builder, "_ensure_schema_exists") as ensure_schema_exists_mock:
            with patch.object(self.schema_builder, "_build_tables") as build_tables_mock:
                with patch.object(
                    self.schema_builder, "_update_prefill_base_tables"
                ) as update_prefill_base_tables_mock:
                    self.schema_builder.build_schema(self.query_executor_mock)
                    ensure_schema_exists_mock.assert_called_once_with(schema=None)
                    build_tables_mock.assert_called_once_with()
                    update_prefill_base_tables_mock.assert_called_once_with()


    # TODO: This could be improved to check if all the tables exist...
    #  however I checked manually and I have a lot to do so I am not implementing this test.

if __name__ == "__main__":
    unittest.main()
