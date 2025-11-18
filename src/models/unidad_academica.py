from typing import Optional
from pydantic import BaseModel
from .objectid import MongoModel, PyObjectId


class UnidadAcademicaBase(BaseModel):
    nombre: str
    facultad_id: PyObjectId


class UnidadAcademicaCreate(UnidadAcademicaBase):
    pass


class UnidadAcademicaUpdate(BaseModel):
    nombre: Optional[str] = None
    facultad_id: Optional[PyObjectId] = None


class UnidadAcademicaOut(UnidadAcademicaBase, MongoModel):
    pass
