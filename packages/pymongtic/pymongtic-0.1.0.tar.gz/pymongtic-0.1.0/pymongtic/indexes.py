from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
import pymongo
from pymongo.errors import OperationFailure

from .base import PymongticModel
from .connect import get_collection


def initialize_indexes():
    for model in __model_registry__:
        if model.Config.view is None:
            collection = get_collection(model.Config.collection_name)
            for ind in model.Config.indexes:
                ind.apply(collection)
        else:
            try:
                model.Config.view.create()
            except OperationFailure as err:
                if err.code != 48:
                    raise err

__model_registry__: List[PymongticModel] = []


class IndexSortDirection(Enum):
    ASCENDING = pymongo.ASCENDING
    DESCENDING = pymongo.DESCENDING
    GEO2D = pymongo.GEO2D
    GEOSPHERE = pymongo.GEOSPHERE
    HASHED = pymongo.HASHED
    TEXT = pymongo.TEXT


class IndexKey(BaseModel):
    name: str
    direction: IndexSortDirection = IndexSortDirection.ASCENDING


class IndexDefinition(BaseModel):
    extras: Optional[dict]
    name: str
    unique: bool = False
    background: bool = True
    sparse: bool = True
    keys: List[IndexKey]

    def apply(self, collection):
        params = {
            "keys": [(k.name, k.direction.value) for k in self.keys],
            "name": self.name,
            "unique": self.unique,
            "background": self.background,
            "sparse": self.sparse,
        }
        if self.extras:
            params.update(**self.extras)
        collection.create_index(**params)

