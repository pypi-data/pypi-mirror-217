from datetime import datetime
from pathlib import Path
from typing import Callable

import pytest
from blackline.constants import PROJECT_CONFIG_FILE
from blackline.factories.query import QueryFactory
from blackline.models.catalogue import Catalogue
from blackline.models.project_config import ProjectConfig
from blackline.models.template import TemplateParams
from blackline.utils.testing.raw_yaml import (
    dataset_yaml,
    organization_yaml,
    project_yaml,
    resource_yaml,
    sqlite_adapter_yaml,
    system_yaml,
)


@pytest.fixture()
def project_root(
    tmp_path: Path,
) -> Path:
    return tmp_path


@pytest.fixture
def fake_project_name() -> str:
    return "fake-project"


@pytest.fixture
def test_table() -> str:
    return "user"


@pytest.fixture
def profile() -> str:
    return "dev"


@pytest.fixture
def store_name() -> str:
    return "dataset_foo"


@pytest.fixture
def project_config_file() -> Path:
    return Path(PROJECT_CONFIG_FILE)


@pytest.fixture
def start_date() -> datetime:
    return datetime(2023, 1, 1)


@pytest.fixture
def mock_user_data() -> list:
    # fmt: off
    return [
        (datetime(2021, 1, 1), "Dave", "dave@example.com", "12345", True, "127.0.0.1", None),  # noqa: E501
        (datetime(2021, 6, 1), "Alison", "alison@example.com", "23456", True, "127.0.0.2", None),  # noqa: E501
        (datetime(2022, 3, 1), "Chris", "chris@example.com", "34567", False, "127.0.0.3", None),  # noqa: E501
        (datetime(2022, 4, 1), "Megan", "megan@example.com", "45678", True, "127.0.0.4", None),  # noqa: E501
        (datetime(2022, 12, 31), "Roy", "Roy@example.com", "45638", True, "127.0.0.5", datetime(2023, 1, 1)),  # noqa: E501
    ]
    # fmt: on


@pytest.fixture
def deidentified_mock_user_data() -> list:
    # fmt: off
    return [
        (datetime(2022, 4, 1, 0, 0), "Megan", "megan@example.com", "45678", 1, "127.0.0.4", None),  # noqa: E501
        (datetime(2022, 3, 1, 0, 0), "Chris", "chris@example.com", "34567", 0, "###.#.#.#", None),  # noqa: E501
        (datetime(2021, 1, 1, 0, 0), None, "fake@email.com", "12345", 1, "###.#.#.#", None),  # noqa: E501
        (datetime(2021, 6, 1, 0, 0), None, "fake@email.com", "23456", 1, "###.#.#.#", None),  # noqa: E501
        (datetime(2022, 12, 31, 0, 0), None, "fake@email.com", "45638", 1, "###.#.#.#", datetime(2023, 1, 1)),  # noqa: E501
    ]
    # fmt: on


@pytest.fixture
def mock_session_data() -> list:
    # fmt: off
    return [
        (datetime(2021, 1, 2), datetime(2021, 1, 3), "dave@example.com", "127.0.0.11", "344DE1ED-B9FB-4B17-960C-F096EA1C05C4"),  # noqa: E501
        (datetime(2021, 1, 3), datetime(2021, 1, 4), "dave@example.com", "127.0.0.11", "BA0F580D-7EE8-4AAA-B105-394A9AFF85FC"),  # noqa: E501
        (datetime(2021, 1, 4), datetime(2021, 1, 5), "dave@example.com", "127.0.0.11", "1F3FDE90-5132-4DCE-A6C3-C630395673B4"),  # noqa: E501
        (datetime(2021, 6, 2), datetime(2021, 6, 3), "alison@example.com", "127.0.0.22", "1DC4FB44-F563-43C3-901F-C968D3896162"),  # noqa: E501
        (datetime(2022, 3, 2), datetime(2022, 3, 3), "chris@example.com", "127.0.0.33", "2EE29388-A9F0-49E3-AE67-798ABB3584CB"),  # noqa: E501
        (datetime(2022, 4, 2), datetime(2022, 4, 3), "megan@example.com", "127.0.0.44", "4C747E07-CE33-46FC-940B-7B8AFB4EFCFA"),  # noqa: E501
        (datetime(2022, 4, 5), datetime(2022, 4, 6), "megan@example.com", "127.0.0.44", "1D268CF9-53B7-4D5E-9333-3DD97341AA28"),  # noqa: E501
    ]
    # fmt: on


@pytest.fixture()
def sample_project(
    test_table: str,
    project_config_file: Path,
    create_project_config: None,
    create_adapter_folder: None,
    create_catalogue_folder: None,
) -> None:
    pass


@pytest.fixture
def project_config(
    project_root: Path,
    project_config_file: Path,
    sample_project: Callable,
) -> ProjectConfig:
    return ProjectConfig.parse_config_file(path=Path(project_root, project_config_file))


@pytest.fixture
def catalogue(project_config: ProjectConfig) -> Catalogue:
    path = Path(project_config.project_root, project_config.catalogue_path)
    return Catalogue.parse_dir(path=path)


@pytest.fixture
def query_factory_factory(
    catalogue: Catalogue,
    test_table: str,
    start_date: datetime,
    store_name: str,
) -> Callable:
    def _query_factory_factory(template_params: TemplateParams) -> QueryFactory:
        store_catalogue = catalogue[
            "organization_foo.system_foo.resource_foo.dataset_foo"
        ]

        collection = [
            collection
            for collection in store_catalogue.collections.values()
            if collection.name == test_table
        ][0]

        return QueryFactory(
            template_params=template_params,
            collection=collection,
            start_date=start_date,
            where_clause=collection.where,
        )

    return _query_factory_factory


@pytest.fixture
def catalogue_dir(tmp_path: Path) -> Path:
    return Path(tmp_path, "catalogue")


@pytest.fixture
def organization_dirs(catalogue_dir: Path) -> list[Path]:
    return [
        Path(catalogue_dir, "organization_foo"),
        Path(catalogue_dir, "organization_bar"),
    ]


@pytest.fixture
def system_dirs(organization_dirs: list[Path]) -> list[Path]:
    return [
        Path(organization_dirs[0], "system_foo"),
        Path(organization_dirs[0], "system_bar"),
    ]


@pytest.fixture
def resource_dirs(system_dirs: list[Path]) -> list[Path]:
    return [
        Path(system_dirs[0], "resource_foo"),
        Path(system_dirs[0], "resource_bar"),
    ]


@pytest.fixture
def dataset_dirs(resource_dirs: list[Path]) -> list[Path]:
    return [
        Path(resource_dirs[0], "dataset_foo"),
        Path(resource_dirs[0], "dataset_bar"),
    ]


@pytest.fixture
def create_catalogue_folder(
    tmp_path: Path,
    catalogue_dir: Path,
    organization_dirs: list[Path],
    system_dirs: list[Path],
    resource_dirs: list[Path],
    dataset_dirs: list[Path],
    test_table: str,
) -> None:
    catalogue_dir.mkdir(exist_ok=True)
    for organization_dir in organization_dirs:
        organization_dir.mkdir(exist_ok=True)
    for system_dir in system_dirs:
        system_dir.mkdir(exist_ok=True)
    for resource_dir in resource_dirs:
        resource_dir.mkdir(exist_ok=True)
    for dataset_dir in dataset_dirs:
        dataset_dir.mkdir(exist_ok=True)

    Path(
        organization_dirs[0],
        "organization.yml",
    ).write_text(organization_yaml())

    Path(
        organization_dirs[1],
        "organization.yml",
    ).write_text(organization_yaml())

    Path(
        system_dirs[0],
        "system.yml",
    ).write_text(system_yaml())

    Path(
        system_dirs[1],
        "system.yml",
    ).write_text(system_yaml())
    Path(
        resource_dirs[0],
        "resource.yml",
    ).write_text(resource_yaml())
    Path(
        resource_dirs[1],
        "resource.yml",
    ).write_text(resource_yaml())

    Path(
        dataset_dirs[0],
        "dataset.yml",
    ).write_text(dataset_yaml(table=test_table))

    Path(
        dataset_dirs[1],
        "dataset.yml",
    ).write_text(dataset_yaml(table=test_table))


@pytest.fixture
def create_adapter_folder(tmp_path: Path) -> None:
    adapter_path = Path(
        tmp_path, "adapters", "organization_foo", "system_foo", "resource_foo"
    )
    adapter_path.mkdir(exist_ok=True, parents=True)
    Path(adapter_path, "dataset_foo.yml").write_text(sqlite_adapter_yaml())
    Path(adapter_path, "dataset_bar.yml").write_text(sqlite_adapter_yaml())


@pytest.fixture
def create_project_config(tmp_path: Path, project_config_file: Path) -> None:
    Path(tmp_path, project_config_file).write_text(project_yaml())
