from datetime import datetime, timedelta

from blackline.factories.query import QueryFactory
from blackline.models.catalogue import Catalogue, DatasetCollection, DatasetField
from blackline.models.datastores import DataStore
from blackline.models.sqlite.sqlite import SQLiteDataStore
from yaml import safe_load


def test__init__(
    catalogue: Catalogue, store: DataStore, test_table: str, store_name: str
) -> None:
    """Test init method."""
    # Setup
    store_catalogue = catalogue["organization_foo.system_foo.resource_foo.dataset_foo"]
    collection = [
        collection
        for collection in store_catalogue.collections.values()
        if collection.name == test_table
    ][0]

    # Run
    factory = QueryFactory(template_params=store.template_params, collection=collection)

    # Assert
    assert isinstance(factory, QueryFactory)
    assert factory.collection == collection


def test_queries(query_factory: QueryFactory, test_table: str) -> None:
    """Test query construction."""

    sql_0 = f"""UPDATE {test_table}\nSET\n  email = :email_value,\n  name = null\nWHERE created_at < :cutoff OR deactivation_date IS NOT NULL"""  # noqa E501
    sql_1 = f"""UPDATE {test_table}\nSET\n  ip = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(ip, '0', :ip_value), '1', :ip_value), '2', :ip_value), '3', :ip_value), '4', :ip_value), '5', :ip_value), '6', :ip_value), '7', :ip_value), '8', :ip_value), '9', :ip_value)\nWHERE created_at < :cutoff OR deactivation_date IS NOT NULL"""  # noqa E501

    # Run
    queries = tuple(query_factory.queries())

    # Assert
    assert len(queries) == len(query_factory.fields_by_period())
    assert queries[0][0] == sql_0
    assert queries[1][0] == sql_1


def test_columns_by_period(query_factory: QueryFactory) -> None:
    """Test columns by retention period method."""
    # Run
    columns = query_factory.fields_by_period()

    # Assert
    assert isinstance(columns, dict)
    assert len(columns) == 2
    for key, value in columns.items():
        assert isinstance(key, timedelta)
        assert isinstance(value, list)
        for column in value:
            assert isinstance(column, DatasetField)


def test_query_with_where_clause(store: DataStore) -> None:
    # Setup
    start_date = datetime(2023, 6, 21)
    where_statement = "AND status='active'"

    sqlite_datastore_yaml = """
    profiles:
      dev:
        type: sqlite
        config:
          connection:
            database: "file::memory:"
            uri: true
    """
    datastore_obj = safe_load(sqlite_datastore_yaml)["profiles"]["dev"]
    datastore = SQLiteDataStore.parse_obj(datastore_obj)

    collection_yaml = f"""
    key: "foo"
    name: "bar"
    datetime_field:
      name: "created_at"
    where: {where_statement}
    fields:
        - name: "id"
          description: "The unique identifier for the record"
          deidentifier:
            type: redact
          period: P365D
    """
    collection_obj = safe_load(collection_yaml)
    collection = DatasetCollection.parse_obj(collection_obj)

    # Run
    factory = QueryFactory(
        collection=collection,
        template_params=datastore.template_params,
        dialect="sqlite",
        start_date=start_date,
        where_clause=where_statement,
    )  # noqa E501

    queries = list(factory.queries())

    # Assert
    assert len(queries) == 1
    assert (
        queries[0][0]
        == f"""UPDATE {collection.name}\nSET\n  id = null\nWHERE created_at < :cutoff {where_statement}"""  # noqa E501
    )  # noqa E501
