from datetime import datetime, timedelta
from typing import Generator, Optional

import sqlglot
from blackline.models.catalogue import DatasetCollection, DatasetField
from blackline.models.template import TemplateParams
from blackline.query.template import Template


class QueryFactory:
    """Query builder class to build query object."""

    def __init__(
        self,
        collection: DatasetCollection,
        template_params: Optional[TemplateParams] = None,
        dialect: Optional[str] = None,
        start_date: Optional[datetime] = None,
        date_format: str = "%Y-%m-%d",
        where_clause: Optional[str] = None,
    ) -> None:
        """
        _summary_

        Args:
            collection (DatasetCollection): _description_
            start_date (Optional[datetime], optional): _description_. Defaults to None.
            template_params (Optional[TemplateParams], optional): _description_. Defaults to None.  # noqa: E501
            date_format (str, optional): _description_. Defaults to "%Y-%m-%d".
            where_clause (Optional[str], optional): Where clause that will be APPENDED to exisiting WHERE <datetime_field> < :cutoff_date. Defaults to None.
        """
        self.collection = collection
        self.dialect = dialect
        self.start_date = start_date or datetime.now()
        self.date_format = date_format
        self.template = Template(
            trim_blocks=True,
            lstrip_blocks=True,
            params=template_params,
            where=where_clause,
        )

    def queries(
        self,
    ) -> Generator[tuple[str, dict[str, Optional[str]]], None, None]:
        return (
            (
                self.render_sql(fields=fields),
                self.values_from_fields(fields=fields, period=period),
            )
            for period, fields in self.fields_by_period().items()
        )

    def render_sql(self, fields: list[DatasetField]) -> str:
        sql = self.template.template.render(
            table=self.collection.name,
            columns=fields,
            datetime_column=self.collection.datetime_field.name,
        )
        if self.dialect is not None:
            sqlglot.transpile(sql=sql, read=self.dialect)
        return sql

    def values_from_fields(
        self, fields: list[DatasetField], period: timedelta
    ) -> dict[str, Optional[str]]:
        values: dict[str, Optional[str]] = {
            f"{field.name}_value": field.deidentifier.value
            for field in fields
            if field.deidentifier is not None
        }
        values["cutoff"] = self.cutoff_date(period=period).strftime(self.date_format)
        return values

    def cutoff_date(self, period: timedelta) -> datetime:
        """Get cutoff date."""
        return self.start_date - period

    def fields_by_period(self) -> dict[timedelta, list[DatasetField]]:
        """Get columns by retention period."""
        fields: dict[timedelta, list[DatasetField]] = {
            field.period: [
                _field
                for _field in self.collection.fields
                if field.period == _field.period
            ]
            for field in self.collection.fields
        }
        return fields
