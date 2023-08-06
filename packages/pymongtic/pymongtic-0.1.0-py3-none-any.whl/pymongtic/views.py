from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel, Field
import pymongo

from pymongtic.base import db


class LookupStep(BaseModel):
    name: str = "$lookup"
    from_collection: str
    local_field: str
    foreign_field: str
    as_name: str

    def dict(self, *args, **kwargs):
        return {
            "from": self.from_collection,
            "localField": self.local_field,
            "foreignField": self.foreign_field,
            "as": self.as_name,
        }


class FieldProjection(BaseModel):
    field: str
    include: bool = True
    expression: Optional[str]


class ProjectStep(BaseModel):
    name: str = "$project"
    projection: List[FieldProjection]

    def dict(self, *args, **kwargs):
        return {f.field: (f.expression if f.expression else (1 if f.include else 0)) for f in self.projection}




class MergeObjects(BaseModel):
    name: str = "$mergeObjects"
    documents: List[Union[dict, str]]

    def dict(self, *args, **kwargs):
        return self.documents



class DocumentProjection(BaseModel):
    fields: List[Union[MergeObjects, FieldProjection]]

    def dict(self, *args, **kwargs):
        result = {}
        for field in self.fields:
            if isinstance(field, MergeObjects):
                result[field.name] = field.dict()
            else:
                result[field.field] = (field.expression if field.expression else (1 if field.include else 0))
        return result


class RemoveFieldsStep(BaseModel):
    name: str = "$unset"
    fields: List[str]

    def dict(self, *args, **kwargs):
        return self.fields


class UnwindStep(BaseModel):
    name: str = "$unwind"
    field: str

    def dict(self, *args, **kwargs):
        return self.field


class ReplaceWithStep(BaseModel):
    name: str = "$replaceWith"
    document: DocumentProjection

    def dict(self, *args, **kwargs):
       return self.document.dict()


class ArbitrayStep(BaseModel):
    name: str = "$replaceWith"
    contents: dict

    def dict(self, *args, **kwargs):
       return self.contents



class View(BaseModel):
    view: str
    source: str
    pipeline: List[Union[
        LookupStep,
        ProjectStep,
        UnwindStep,
        RemoveFieldsStep,
        ReplaceWithStep,
        ArbitrayStep,
    ]]

    def dict(self, *args, **kwargs):
        return {
            "create": self.view,
            "viewOn": self.source, 
            "pipeline": [{step.name: step.dict()} for step in self.pipeline], 
        }

    def create(self):
        db.command(self.dict())
