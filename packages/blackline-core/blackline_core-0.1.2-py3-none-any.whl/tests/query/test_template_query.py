import sqlglot
from blackline.models.catalogue import DatasetField, Redact
from blackline.models.datastores import DataStore
from blackline.query.template import Template
from jinja2.runtime import Macro


def test__init__(store: DataStore) -> None:
    # Run
    template = Template(params=store.template_params)

    # Assert
    assert isinstance(template, Template)
    assert isinstance(template.env.globals["redact"], Macro)
    assert isinstance(template.env.globals["replace"], Macro)
    assert isinstance(template.env.globals["mask"], Macro)


def test_template_str(store: DataStore) -> None:
    # Setup
    template = Template(params=store.template_params)
    expected = """UPDATE {{ table }}\nSET\n{% for column in columns %}\n  {% set value = column.name + "_value" %}\n  {{ redact(cls=column.deidentifier, name=column.name, value=value) -}}\n  {{ replace(cls=column.deidentifier, name=column.name, value=value) -}}\n  {{ mask(cls=column.deidentifier, name=column.name, value=value) -}}\n  {{ "," if not loop.last }}\n{% endfor %}\nWHERE {{ datetime_column }} < :cutoff\n"""  # noqa E501

    # Run
    _template = template.template_str()

    # Assert
    assert _template == expected


def test_template_render(store: DataStore) -> None:
    # Setup
    template = Template(params=store.template_params)
    table = "test_table"
    column_names = ["foo_redact"]
    columns = [
        DatasetField(
            name=column_names[0], deidentifier=Redact(type="redact"), period="P365D"
        ),
    ]
    datetime_column = "created_at"

    # Run
    sql = template.template.render(
        table=table, columns=columns, datetime_column=datetime_column
    )

    # Assert
    assert (
        sql
        == f"UPDATE {table}\nSET\n  {column_names[0]} = null\nWHERE {datetime_column} < :cutoff"  # noqa E501
    )
    assert sqlglot.parse(sql) is not None


def test_template_render_with_where(store: DataStore) -> None:
    # Setup
    table = "test_table"
    column_names = ["foo_redact"]
    columns = [
        DatasetField(
            name=column_names[0], deidentifier=Redact(type="redact"), period="P365D"
        ),
    ]
    datetime_column = "created_at"
    where = "AND foo = 'bar'"
    template = Template(params=store.template_params, where=where)
    # Run
    sql = template.template.render(
        table=table, columns=columns, datetime_column=datetime_column
    )

    # Assert
    assert (
        sql
        == f"UPDATE {table}\nSET\n  {column_names[0]} = null\nWHERE {datetime_column} < :cutoff {where}"  # noqa E501
    )
    assert sqlglot.parse(sql) is not None
