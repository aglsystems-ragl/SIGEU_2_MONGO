from typing import Optional
from pydantic import BaseModel
from .objectid import MongoModel


class LugarBase(BaseModel):
    ubicacion: str
    capacidad: int
    tipo: str  # auditorio, salon, laboratorio, cancha


class LugarCreate(LugarBase):
    pass


class LugarUpdate(BaseModel):
    ubicacion: Optional[str] = None
    capacidad: Optional[int] = None
    tipo: Optional[str] = None


class LugarOut(LugarBase, MongoModel):
    pass
