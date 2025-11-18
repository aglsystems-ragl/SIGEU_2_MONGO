from typing import Optional
from pydantic import BaseModel
from .objectid import MongoModel, PyObjectId


class FacultadBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None


class FacultadCreate(FacultadBase):
    pass


class FacultadUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None


class FacultadOut(MongoModel):
    nombre: str
    telefono: str
