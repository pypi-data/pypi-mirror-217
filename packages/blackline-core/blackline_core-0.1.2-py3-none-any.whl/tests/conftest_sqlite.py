import sqlite3
from sqlite3 import Connection

import pytest
from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.models.datastores import DataStore


@pytest.fixture
def sqlite_store_name() -> str:
    return "test_sqlite"


@pytest.fixture
def deidentified_mock_data_sqlite(deidentified_mock_user_data: list) -> list:
    return [
        (
            user[0].strftime("%Y-%m-%d %H:%M:%S"),
            user[1],
            user[2],
            user[3],
            int(user[4]),
            user[5],
            user[6].strftime("%Y-%m-%d %H:%M:%S") if user[6] is not None else None,
        )
        for user in deidentified_mock_user_data
    ]


@pytest.fixture
def mock_sqlite_store(
    mock_user_data: list, test_table: str, mock_session_data: list
) -> Connection:
    con = sqlite3.connect(
        "file::memory:?cache=shared",
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        uri=True,
    )

    with con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {test_table}")
        cur.execute(
            f"""CREATE TABLE {test_table}(
                created_at TEXT,
                name TEXT,
                email TEXT,
                postal_code TEXT,
                active BOOLEAN,
                ip TEXT,
                deactivation_date TEXT
                )"""
        )

        cur.executemany(
            f"INSERT INTO {test_table} VALUES (?, ?, ?, ?, ?, ?, ?)", mock_user_data
        )

    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS session")
        cur.execute(
            """CREATE TABLE session(
            created_at TEXT,
            session_started_at TEXT,
            email TEXT,
            ip TEXT,
            cookie_id TEXT
            )"""
        )
        cur.executemany("INSERT INTO session VALUES (?, ?, ?, ?, ?)", mock_session_data)

    yield con

    with con:
        con.cursor().execute("DROP TABLE session")

    with con:
        con.cursor().execute(f"DROP TABLE {test_table}")

    con.close()


@pytest.fixture
def sqlite_adapter(
    store: DataStore, mock_sqlite_store: Connection, store_name: str
) -> SQLiteAdapter:
    return store.adapter


@pytest.fixture
def sqlite_store_profiles_yaml() -> str:
    return """
    profiles:
      dev:
        type: sqlite
        config:
          connection:
            database: "file::memory:"
            uri: true
    """
