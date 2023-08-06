import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Union, Mapping, Sequence, Dict, Any

from pydantic import BaseModel, BaseConfig, Field
from bson import ObjectId
# from bson.raw_bson import RawBSONDocument
from dateutil.tz import UTC

from .connect import db, get_collection
from .exceptions import ReadOnlyViewError



def NOW():
    return datetime.datetime.now(tz=UTC)


class OID(ObjectId):
    """ Custom Type for reading MongoDB IDs """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class PymongticModel(BaseModel):
    id: Optional[Union[OID, str, None]] = Field(alias='_id')
    created: Optional[datetime.datetime]
    last_modified: Optional[datetime.datetime]

    class Config(BaseConfig):
        collection_name = "collection"
        indexes = []
        view = None
        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime.datetime: lambda dt: dt.isoformat(),
            datetime.date: lambda dt: dt.isoformat(),
            ObjectId: str,
            OID: str,
            Enum: lambda e: e.value,
            Decimal: str,
        }

    @classmethod
    def from_mongo(cls, data: dict, no_validation: bool=False):
        """We must convert _id into "id". """
        if not data:
            return data
        _id = data.pop('_id', None)
        if no_validation:
            return cls.construct(**data)
        return cls(**dict(data, id=str(_id)))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        if not hasattr(self, "id") or self.id is None:
            self.created = datetime.datetime.now(tz=UTC)
        else:
            self.last_modified = datetime.datetime.now(tz=UTC)

        parsed = self.dict(
            exclude_none=False,
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        return self.__prepare_fields_for_mongo(parsed)
    
    def __prepare_fields_for_mongo(self, obj:Mapping) -> Mapping:
        result = {}
        for key in obj:
            result[key] = self.__prepare_field_for_mongo(obj[key])
        return result

    def __prepare_field_for_mongo(self, val:any) -> any:
        if isinstance(val, Mapping):
            return self.__prepare_fields_for_mongo(val)
        elif not isinstance(val, (str, bytes)) and isinstance(val, Sequence):
            nval = []
            for item in val:
                if isinstance(val, Mapping):
                    nval.append(self.__prepare_fields_for_mongo(val))
                else:
                    nval.append(self.__prepare_field_for_mongo(item))
            return nval
        elif isinstance(val, Enum):
            return val.value
        val_type = type(val)
        if val_type is not ObjectId and val_type in self.Config.json_encoders:
            return self.Config.json_encoders[val_type](val)
        return val
    
    @property
    def collection(self):
        return get_collection(self.Config.collection_name)

    def save(self, upsert: bool=False, result_class: Optional[type[BaseModel]]=None):
        if self.Config.view is not None:
            raise ReadOnlyViewError("read only view")
        collection = self.collection
        if not hasattr(self, "id") or self.id is None:
            insertable = self.mongo()
            if "_id" in insertable:
                del insertable["_id"]
            response = collection.insert_one(insertable)
            if result_class is None:
                if hasattr(self, "id"):
                    self.id = str(response.inserted_id)
                return self
            return result_class(id=str(response.inserted_id), **self.dict())
        elif upsert:
            response = collection.replace_one({"_id": self.id}, self.mongo(), upsert=True)
            if result_class is None:
                return self
            return result_class(**self.dict())
        else:
            response = collection.update_one({"_id": self.id}, {"$set": self.mongo()})
            if result_class is None:
                return self
            if hasattr(self, "id"):
                return result_class(**self.dict())
            else:
                return result_class(**self.dict())

    def delete(self, query_fields: List[str]=None):
        if self.Config.view is not None:
            raise ReadOnlyViewError("read only view")
        filter = {}
        if query_fields is None:
            filter["_id"] = self.id
        else:
            for field_name in query_fields:
                filter[field_name] = getattr(self, field_name)
        collection = get_collection(self.Config.collection_name)
        result = collection.delete_one(filter)
        return result.deleted_count > 0

    
    @classmethod
    def patch_one(self, id: OID, patch: dict):
        pass

    @classmethod
    def find_one(cls, filter: dict, no_validation: bool=False, *args, **kwargs):
        collection = get_collection(cls.Config.collection_name if cls.Config.view is None else cls.Config.view.view)
        one = collection.find_one(filter=filter, *args, **kwargs)
        if one:
            return cls.from_mongo(one, no_validation)
        return None

    @classmethod
    def find(cls, filter: dict, *args, **kwargs):
        collection = get_collection(cls.Config.collection_name if cls.Config.view is None else cls.Config.view.view)
        some = collection.find(filter=filter, *args, **kwargs)
        results = []
        for one in some:
            results.append(cls.from_mongo(one))
        return results
