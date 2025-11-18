from typing import Optional
from pydantic import BaseModel
from .objectid import MongoModel


class OrganizacionExternaBase(BaseModel):
    nombre: str
    nombre_representante_legal: str
    ubicacion: str
    sector_economico: str
    actividad_principal: str
    numero_contacto: str


class OrganizacionExternaCreate(OrganizacionExternaBase):
    pass


class OrganizacionExternaUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_representante_legal: Optional[str] = None
    ubicacion: Optional[str] = None
    sector_economico: Optional[str] = None
    actividad_principal: Optional[str] = None
    numero_contacto: Optional[str] = None


class OrganizacionExternaOut(OrganizacionExternaBase, MongoModel):
    pass
