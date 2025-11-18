from typing import Optional
from pydantic import BaseModel
from .objectid import MongoModel, PyObjectId


class ProgramaAcademicoBase(BaseModel):
    nombre: str
    facultad_id: PyObjectId


class ProgramaAcademicoCreate(ProgramaAcademicoBase):
    pass


class ProgramaAcademicoUpdate(BaseModel):
    nombre: Optional[str] = None
    facultad_id: Optional[PyObjectId] = None


class ProgramaAcademicoOut(ProgramaAcademicoBase, MongoModel):
    pass
