import os
from typing import List

import pytest
import yaml
from blackline.adapters.mysql.mysql import MySQLAdapter
from blackline.factories.query import QueryFactory
from blackline.models.datastores import DataStore
from blackline.models.mysql.mysql import MySQLDataStore
from mysql.connector import MySQLConnection


def test_mysql_store_config(stores_yaml: str):
    # Setup
    pg_store_info = yaml.safe_load(stores_yaml)

    # Run
    store_config = DataStore.parse_obj(pg_store_info)

    # Assert
    isinstance(store_config.profiles["dev"], MySQLDataStore)


def test_query_factory_mysql_queries(
    mysql_query_factory: QueryFactory, test_table: str
):
    # Run
    queries = tuple(mysql_query_factory.queries())

    # Assert
    assert (
        queries[0][0]
        == f"UPDATE {test_table}\nSET\n  email = %(email_value)s,\n  name = null\nWHERE created_at < %(cutoff)s OR deactivation_date IS NOT NULL"  # noqa: E501
    )
    assert (
        queries[1][0]
        == f"UPDATE {test_table}\nSET\n  ip = REGEXP_REPLACE(ip,'[:alnum:]',%(ip_value)s)\nWHERE created_at < %(cutoff)s OR deactivation_date IS NOT NULL"  # noqa: E501
    )


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Github Actions does not have a local mysql",
)
def test_query_factory_mysql_execution(
    load_database: MySQLConnection,
    mysql_query_factory: QueryFactory,
    test_table: str,
    deidentified_mock_user_data: List,
    mysql_adapter: MySQLAdapter,
):
    # Run
    queries = tuple(mysql_query_factory.queries())
    mysql_adapter.execute(sql=queries[0][0], values=queries[0][1])
    mysql_adapter.execute(sql=queries[1][0], values=queries[1][1])

    # Assert
    with mysql_adapter.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {test_table}")
            rows = cursor.fetchall()

    # Remove the UUIS from the rows
    rows = [row[1:] for row in rows]

    assert set(deidentified_mock_user_data) == set(rows)
