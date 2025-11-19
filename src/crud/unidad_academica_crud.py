from bson import ObjectId
from fastapi import HTTPException
from typing import List
from src.db.client import db
from src.models.unidad_academica import (
    UnidadAcademicaCreate,
    UnidadAcademicaOut,
    UnidadAcademicaUpdate,
)

collection = db["unidad_academica"]


def _to_out(doc) -> UnidadAcademicaOut:
    """
    Convierte el documento de MongoDB a el modelo de salida UnidadAcademicaOut.

    - Pasa `_id` -> `id` como string.
    - Convierte `facultad_id` (ObjectId) a string para que Pydantic
      pueda validarlo como PyObjectId sin error.
    """
    doc = dict(doc)

    # _id de Mongo -> id (string)
    doc["id"] = str(doc.pop("_id"))

    # MUY IMPORTANTE: convertir facultad_id a str
    if "facultad_id" in doc and not isinstance(doc["facultad_id"], str):
        doc["facultad_id"] = str(doc["facultad_id"])

    return UnidadAcademicaOut(**doc)


async def create_unidad_academica_crud(
    data: UnidadAcademicaCreate,
) -> UnidadAcademicaOut:
    payload = data.model_dump()
    result = await collection.insert_one(payload)
    new_doc = await collection.find_one({"_id": result.inserted_id})
    return _to_out(new_doc)


async def get_unidad_academica_crud(id: str) -> UnidadAcademicaOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(
            status_code=404, detail="Unidad académica no encontrado"
        )

    return _to_out(doc)


async def list_unidad_academicas_crud() -> List[UnidadAcademicaOut]:
    docs: List[UnidadAcademicaOut] = []
    cursor = collection.find({})

    async for d in cursor:
        docs.append(_to_out(d))

    return docs


async def update_unidad_academica_crud(
    id: str, data: UnidadAcademicaUpdate
) -> UnidadAcademicaOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    payload = data.model_dump(exclude_unset=True)

    # Si no hay nada que actualizar
    if not payload:
        raise HTTPException(
            status_code=400,
            detail="No hay datos para actualizar",
        )

    result = await collection.update_one({"_id": oid}, {"$set": payload})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail="Unidad académica no encontrado"
        )

    doc = await collection.find_one({"_id": oid})
    return _to_out(doc)


async def delete_unidad_academica_crud(id: str) -> dict:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await collection.delete_one({"_id": oid})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Unidad académica no encontrado"
        )

    return {"msg": "Unidad académica eliminado"}
