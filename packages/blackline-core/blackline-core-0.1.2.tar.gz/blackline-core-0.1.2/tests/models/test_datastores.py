from pathlib import Path

import pytest
from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.models.datastore_base import DataStoreBase
from blackline.models.datastores import DataStore, DataStores
from blackline.models.project_config import ProjectConfig
from blackline.models.sqlite.sqlite import SQLiteDataStore
from yaml import safe_load


def test_DataStore(profile: str, sqlite_store_profiles_yaml: str) -> None:
    # Setup
    info = safe_load(sqlite_store_profiles_yaml)
    info["name"] = "foo"

    # Run
    config = DataStore.parse_obj(info)

    # Assert
    assert config.name == "foo"
    assert isinstance(config.profiles[profile], SQLiteDataStore)


def test_DataStores(profile: str, sqlite_store_profiles_yaml: str) -> None:
    # Setup
    info = safe_load(sqlite_store_profiles_yaml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)

    # Run
    stores = DataStores(stores=[config])

    # Assert
    for store in stores.stores:
        assert isinstance(store, DataStore)


def test_DataStores_store_with_profile(
    profile: str, sqlite_store_profiles_yaml: str
) -> None:
    # Setup
    info = safe_load(sqlite_store_profiles_yaml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])

    # Run
    store = stores["foo"][profile]

    # Assert
    assert isinstance(store, SQLiteDataStore)


def test_DataStores_store_no_profile(
    profile: str, sqlite_store_profiles_yaml: str
) -> None:
    # Setup
    info = safe_load(sqlite_store_profiles_yaml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])

    # Run
    store = stores["foo"]

    # Assert
    assert isinstance(store, DataStore)


def test_DataStores_store_not_found(
    profile: str, sqlite_store_profiles_yaml: str
) -> None:
    # Setup
    info = safe_load(sqlite_store_profiles_yaml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])

    # Run
    with pytest.raises(ValueError) as excinfo:
        stores["bar"]

        # Assert
        assert "Store bar not found" in str(excinfo.value)


def test_DataStores_parse_folder(
    project_config: ProjectConfig, profile: str, store_name: str
):
    path = Path(project_config.project_root, project_config.adapters_path)

    # Run
    stores = DataStores.parse_folder(path=path)
    store = stores[store_name][profile]

    # Assert
    assert isinstance(store, DataStoreBase)
    assert isinstance(store.adapter, SQLiteAdapter)
    assert store.config.connection.database == "file::memory:?cache=shared"
