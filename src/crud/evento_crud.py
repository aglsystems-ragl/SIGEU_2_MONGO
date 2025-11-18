from typing import List

from bson import ObjectId
from fastapi import HTTPException, status

from src.db.client import db
from src.models.evento import EventoCreate, EventoOut, EventoUpdate

# Colecciones Mongo
COLLECTION = db.evento
USUARIOS = db.usuario


def _to_out(doc) -> EventoOut:
    """
    Convierte un documento crudo de Mongo a EventoOut,
    asegurando que TODOS los ObjectId se convierten a str para la API.
    """
    if not doc:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return EventoOut(
        id=str(doc["_id"]),
        # En la BD no estamos guardando creador_id por el validador,
        # así que normalmente vendrá en None.
        creador_id=str(doc.get("creador_id")) if doc.get("creador_id") else None,
        nombre=doc.get("nombre"),
        descripcion=doc.get("descripcion"),
        fecha_inicio=doc.get("fecha_inicio"),
        fecha_fin=doc.get("fecha_fin"),
        lugar_id=str(doc.get("lugar_id")) if doc.get("lugar_id") else None,
        facultad_id=str(doc.get("facultad_id")) if doc.get("facultad_id") else None,
        unidad_academica_id=str(doc.get("unidad_academica_id")) if doc.get("unidad_academica_id") else None,
        programa_academico_id=str(doc.get("programa_academico_id")) if doc.get("programa_academico_id") else None,
        organizacion_externa_id=(
            str(doc.get("organizacion_externa_id"))
            if doc.get("organizacion_externa_id") is not None
            else None
        ),
    )


# ==============================
#  CRUD ASÍNCRONO DE EVENTOS
# ==============================

async def list_eventos_crud() -> List[EventoOut]:
    """
    Lista todos los eventos.
    Usa 'async for' porque COLLECTION.find() devuelve un AsyncIOMotorCursor.
    """
    eventos: List[EventoOut] = []
    cursor = COLLECTION.find()
    async for doc in cursor:
        eventos.append(_to_out(doc))
    return eventos


async def get_evento_crud(item_id: str) -> EventoOut:
    """
    Obtiene un evento por su _id.
    """
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de evento inválido",
        )

    doc = await COLLECTION.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return _to_out(doc)


async def create_evento_crud(payload: EventoCreate) -> EventoOut:
    """
    Crea un nuevo evento a partir del EventoCreate recibido desde la API.

    Lógica de negocio importante (emulación de trigger):
      1. Valida que 'creador_id' sea un ObjectId válido.
      2. Busca el usuario en la colección `usuario`.
      3. Verifica que su rol sea 'docente' o 'estudiante'.
         - Si NO lo es, lanza HTTP 403 (forbidden) y NO crea el evento.

    Por compatibilidad con el validador JSON Schema de la colección `evento`,
    NO guardamos el campo 'creador_id' dentro del documento, solo lo usamos
    para validar el permiso de creación.
    """
    data = payload.model_dump()

    # 1) Validar y convertir el creador_id
    try:
        creador_oid = ObjectId(data["creador_id"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="creador_id no es un ObjectId válido",
        )

    # 2) Buscar el usuario creador
    usuario_doc = await USUARIOS.find_one({"_id": creador_oid})
    if not usuario_doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario creador no existe en la colección 'usuario'",
        )

    rol = usuario_doc.get("rol")
    # 3) Validar rol
    if rol not in ("docente", "estudiante"):
        # Aquí emulamos la lógica del trigger:
        # solo docente o estudiante pueden crear eventos.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo usuarios con rol 'docente' o 'estudiante' pueden crear eventos",
        )

    # 4) Convertir el resto de IDs relacionados (estos sí van a la colección evento)
    try:
        insert_doc = {
            # OJO: NO incluimos 'creador_id' para no romper el validador de Mongo.
            "nombre": data["nombre"],
            "descripcion": data.get("descripcion"),
            "fecha_inicio": data["fecha_inicio"],
            "fecha_fin": data["fecha_fin"],
            "lugar_id": ObjectId(data["lugar_id"]),
            "facultad_id": ObjectId(data["facultad_id"]),
            "unidad_academica_id": ObjectId(data["unidad_academica_id"]),
            "programa_academico_id": ObjectId(data["programa_academico_id"]),
            "organizacion_externa_id": (
                ObjectId(data["organizacion_externa_id"])
                if data.get("organizacion_externa_id")
                else None
            ),
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alguno de los ids relacionados del evento no es un ObjectId válido",
        )

    # 5) Insertar en Mongo
    result = await COLLECTION.insert_one(insert_doc)
    new_doc = await COLLECTION.find_one({"_id": result.inserted_id})
    return _to_out(new_doc)


async def update_evento_crud(item_id: str, payload: EventoUpdate) -> EventoOut:
    """
    Actualiza parcialmente un evento.
    Solo actualiza los campos que vienen en el body (no None).
    """
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de evento inválido",
        )

    data = {k: v for k, v in payload.model_dump().items() if v is not None}

    # NO permitimos cambiar el creador desde este endpoint (aunque no se guarda).
    data.pop("creador_id", None)

    # Convertir ids de string a ObjectId si vienen en la actualización
    try:
        if "lugar_id" in data:
            data["lugar_id"] = ObjectId(data["lugar_id"])
        if "facultad_id" in data:
            data["facultad_id"] = ObjectId(data["facultad_id"])
        if "unidad_academica_id" in data:
            data["unidad_academica_id"] = ObjectId(data["unidad_academica_id"])
        if "programa_academico_id" in data:
            data["programa_academico_id"] = ObjectId(data["programa_academico_id"])
        if "organizacion_externa_id" in data:
            data["organizacion_externa_id"] = (
                ObjectId(data["organizacion_externa_id"])
                if data["organizacion_externa_id"] is not None
                else None
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alguno de los ids relacionados del evento no es un ObjectId válido",
        )

    result = await COLLECTION.update_one(
        {"_id": oid},
        {"$set": data},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    updated = await COLLECTION.find_one({"_id": oid})
    return _to_out(updated)


async def delete_evento_crud(item_id: str) -> dict:
    """
    Elimina un evento por id.
    """
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id de evento inválido",
        )

    result = await COLLECTION.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return {"message": "Evento eliminado correctamente"}
