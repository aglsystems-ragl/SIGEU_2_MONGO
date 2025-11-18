from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic import ConfigDict


# =========================================
#  MODELOS BASE (ENTRADA / CREACIÓN)
# =========================================

class EventoBase(BaseModel):
    """
    Modelo base para creación de eventos.
    Aquí pedimos los campos obligatorios cuando se CREA un evento.
    """

    # Quién crea el evento (referencia a colección `usuario`)
    creador_id: str = Field(
        ...,
        description="Id del usuario que crea el evento (colección usuario). "
                    "Solo se permitirá si su rol es 'docente' o 'estudiante'."
    )

    nombre: str = Field(..., description="Nombre del evento")
    descripcion: Optional[str] = Field(
        None, description="Descripción breve del evento"
    )
    fecha_inicio: datetime = Field(
        ..., description="Fecha y hora de inicio del evento"
    )
    fecha_fin: datetime = Field(
        ..., description="Fecha y hora de finalización del evento"
    )

    # IDs de otras colecciones (como string de ObjectId en la API)
    lugar_id: str = Field(..., description="Id del lugar (colección lugar)")
    facultad_id: str = Field(..., description="Id de la facultad organizadora")
    unidad_academica_id: str = Field(
        ..., description="Id de la unidad académica responsable"
    )
    programa_academico_id: str = Field(
        ..., description="Id del programa académico asociado"
    )
    organizacion_externa_id: Optional[str] = Field(
        None, description="Id de la organización externa (si aplica)"
    )

    model_config = ConfigDict(from_attributes=True)


class EventoCreate(EventoBase):
    """
    Modelo para crear eventos.
    Igual a EventoBase (todos obligatorios excepto descripción y organización externa).
    """
    pass


# =========================================
#  MODELO PARA ACTUALIZAR
# =========================================

class EventoUpdate(BaseModel):
    """
    Modelo para actualizar eventos.
    Todos los campos son opcionales (parche parcial).
    """
    # Normalmente no se cambia el creador, por eso no lo incluimos aquí.
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar_id: Optional[str] = None
    facultad_id: Optional[str] = None
    unidad_academica_id: Optional[str] = None
    programa_academico_id: Optional[str] = None
    organizacion_externa_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =========================================
#  MODELO DE SALIDA (RESPUESTA API)
# =========================================

class EventoOut(BaseModel):
    """
    Modelo para RESPUESTAS de la API.
    Aquí permitimos que algunos campos sean None,
    para poder mapear documentos antiguos o incompletos sin que Pydantic falle.
    """
    id: str = Field(..., description="Id del evento en MongoDB")

    # Usuario que creó el evento
    creador_id: Optional[str] = Field(
        None,
        description="Id del usuario que creó el evento (colección usuario)"
    )

    # Los siguientes pueden venir en None si el documento en Mongo está incompleto
    nombre: Optional[str] = Field(None, description="Nombre del evento")
    descripcion: Optional[str] = Field(
        None, description="Descripción breve del evento"
    )
    fecha_inicio: Optional[datetime] = Field(
        None, description="Fecha y hora de inicio del evento"
    )
    fecha_fin: Optional[datetime] = Field(
        None, description="Fecha y hora de finalización del evento"
    )

    lugar_id: Optional[str] = Field(
        None, description="Id del lugar (colección lugar)"
    )
    facultad_id: Optional[str] = Field(
        None, description="Id de la facultad organizadora"
    )
    unidad_academica_id: Optional[str] = Field(
        None, description="Id de la unidad académica responsable"
    )
    programa_academico_id: Optional[str] = Field(
        None, description="Id del programa académico asociado"
    )
    organizacion_externa_id: Optional[str] = Field(
        None, description="Id de la organización externa (si aplica)"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
