from datetime import datetime
from typing import Any

from blackline.factories.adapter import AdapterFactory
from blackline.factories.query import QueryFactory
from blackline.models.catalogue import Dataset, DatasetCollection
from blackline.models.template import TemplateParams
from pydantic import BaseModel, root_validator, validator


class ConnectionConfig(BaseModel):
    ...


class DataStoreBase(BaseModel):
    type: str
    adapter: Any = None

    @validator("adapter", pre=True, always=True)
    def load_adapter_cls(cls, value, values):
        return AdapterFactory.load_adapter(name=values["type"])

    @root_validator(pre=False)
    def initialize_adapter(cls, values):
        """
        Shit design patter. The values["config"] is only added by the subclass.
        This model cannot exist on it's on and is not labeled as an ABC.
        """
        values["adapter"] = values["adapter"](values["config"])
        return values

    @property
    def template_params(self):
        return TemplateParams(
            update_template=self.adapter.update_template(),
            set_template=self.adapter.set_template(),
            where_template=self.adapter.where_template(),
            redact_template=self.adapter.redact_template(),
            replace_template=self.adapter.replace_template(),
            mask_template=self.adapter.mask_template(),
        )

    def deidentify(self, dataset: Dataset, start_date: datetime = datetime.now()):
        for collection in dataset.collections.values():
            self.deidentify_collection(collection=collection, start_date=start_date)

    def deidentify_collection(
        self, collection: DatasetCollection, start_date: datetime = datetime.now()
    ):
        query_factory = QueryFactory(
            collection=collection,
            template_params=self.template_params,
            dialect=self.adapter.dialect,
            start_date=start_date,
            where_clause=collection.where,
        )
        for sql, values in query_factory.queries():
            self.adapter.execute(sql, values)
