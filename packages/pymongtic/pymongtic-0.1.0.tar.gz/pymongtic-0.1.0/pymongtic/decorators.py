from typing import List
from .indexes import __model_registry__


def pymongtic_model(collection_name: str = None):
    """
    Decorator that registers a model with pymongtic so that indexes
    and views can be setup when `initialize_indexes` is called.
    """
    def inner(cls):
        if collection_name:
            cls.Config.collection_name = collection_name
        __model_registry__.append(cls)
        return cls
    return inner


def no_timestamps(cls):
    """
    Decorator that removes the timestamp fields from the model class.
    """
    del cls.__fields__["created"]
    del cls.__fields__["last_modified"]
    return cls


def no_id(cls):
    """
    Decorator that removes the timestamp fields from the model class.
    """
    if "id" in cls.__fields__:
        del cls.__fields__["id"]
    if "_id" in cls.__fields__:
        del cls.__fields__["_id"]
    return cls



def remove_fields(fields:List[str]):
    """
    Decorator that removes the timestamp fields from the model class.
    """
    def inner(cls):
        for field in fields:
            if field in cls.__fields__:
                del cls.__fields__[field]
        return cls
    return inner
