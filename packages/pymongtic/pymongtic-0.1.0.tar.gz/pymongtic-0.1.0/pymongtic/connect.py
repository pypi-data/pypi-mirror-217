from enum import Enum
from functools import lru_cache, wraps

from bson.binary import UuidRepresentation
from bson.codec_options import CodecOptions
from bson.codec_options import TypeRegistry
from dateutil.tz import UTC
import pymongo

from .config import settings


def fallback_encoder(value):
    print("fallback_encoder called")
    if isinstance(value, Enum):
        return str(value.value)
    return value


type_registry = TypeRegistry(fallback_encoder=fallback_encoder)
codec_options = CodecOptions(tz_aware=True, uuid_representation=UuidRepresentation.STANDARD, type_registry=type_registry)



try:
    client = pymongo.MongoClient(settings.mongodb_uri)
except Exception as e:
    print("---------------------------------------")
    print(settings.mongodb_uri)
    print(e)
    print("---------------------------------------")


db = client[settings.mongodb_database_name]

@lru_cache(maxsize=32)
def get_collection(name: str):
    return db[name].with_options(codec_options=CodecOptions(
        tz_aware=True,
        tzinfo=UTC))

