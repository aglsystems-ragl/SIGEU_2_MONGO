from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .objectid import MongoModel, PyObjectId

class RolEnum(str, Enum):
    docente = "docente"
    estudiante = "estudiante"
    secretario = "secretario"

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    rol: RolEnum

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[RolEnum] = None

class UsuarioOut(MongoModel):
    nombre: str
    apellido: str
    correo: EmailStr
    rol: RolEnum