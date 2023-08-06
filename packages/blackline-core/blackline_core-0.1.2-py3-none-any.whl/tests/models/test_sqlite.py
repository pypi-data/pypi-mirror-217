from datetime import datetime
from unittest.mock import MagicMock

import pytest
import sqlglot
from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.models.catalogue import DatasetCollection
from blackline.models.sqlite.sqlite import SQLiteConnectionConfig, SQLiteDataStore
from blackline.models.template import TemplateParams
from pytest import MonkeyPatch
from sqlglot.errors import ParseError
from yaml import safe_load


def test_SQLiteConnectionConfig(profile: str, sqlite_store_profiles_yaml: str) -> None:
    info = safe_load(sqlite_store_profiles_yaml)
    info = info["profiles"][profile]["config"]["connection"]
    config = SQLiteConnectionConfig.parse_obj(info)
    assert config.database == "file::memory:"
    assert config.uri is True


def test_SQLLiteConfig(profile: str, sqlite_store_profiles_yaml: str) -> None:
    info = safe_load(sqlite_store_profiles_yaml)
    sqlite_info = info["profiles"][profile]
    config = SQLiteDataStore.parse_obj(sqlite_info)
    assert config.type == "sqlite"
    isinstance(config.adapter, SQLiteAdapter)


def test_template_params(monkeypatch: MonkeyPatch):
    # Setup
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

    # Run
    template_params = datastore.template_params

    # Assert
    assert isinstance(template_params, TemplateParams)


def test_deidentify_collection(monkeypatch):
    # Setup
    start_date = datetime(2023, 6, 21)

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

    collection_yaml = """
    key: "foo"
    name: "bar"
    datetime_field:
      name: "created_at"
    fields:
        - name: "id"
          description: "The unique identifier for the record"
          deidentifier:
            type: redact
          period: P365D
    """
    collection_obj = safe_load(collection_yaml)
    collection = DatasetCollection.parse_obj(collection_obj)

    monkeypatch.setattr(
        datastore.adapter,
        "execute",
        MagicMock(),
    )

    # Run
    datastore.deidentify_collection(collection=collection, start_date=start_date)

    # Assert
    assert datastore.adapter.execute.assert_called() is None
    sql = datastore.adapter.execute.call_args[0][0]
    assert sqlglot.transpile(sql)


def test_deidentify_collection_with_where(monkeypatch):
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

    monkeypatch.setattr(
        datastore.adapter,
        "execute",
        MagicMock(),
    )

    # Run
    datastore.deidentify_collection(collection=collection, start_date=start_date)

    # Assert
    assert datastore.adapter.execute.assert_called() is None
    assert where_statement in datastore.adapter.execute.call_args[0][0]


def test_deidentify_collection_with_where_and_raises_a_sql_error(monkeypatch):
    # Setup
    start_date = datetime(2023, 6, 21)
    where_statement = "status='active'"

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

    monkeypatch.setattr(
        datastore.adapter,
        "execute",
        MagicMock(),
    )

    # Run & Assert
    with pytest.raises(ParseError):
        datastore.deidentify_collection(collection=collection, start_date=start_date)
