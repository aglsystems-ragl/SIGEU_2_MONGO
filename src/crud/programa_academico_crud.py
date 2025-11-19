from bson import ObjectId
from fastapi import HTTPException
from typing import List

from src.db.client import db
from src.models.programa_academico import (
    ProgramaAcademicoCreate,
    ProgramaAcademicoOut,
    ProgramaAcademicoUpdate,
)

collection = db["programa_academico"]


def _to_out(doc) -> ProgramaAcademicoOut:
    """
    Convierte el documento de MongoDB al modelo de salida ProgramaAcademicoOut.

    - Convierte `_id` de Mongo a `id` (string).
    - Convierte `facultad_id` (ObjectId) a string para que PyObjectId lo acepte.
    """
    doc = dict(doc)

    # _id de Mongo -> id visible para la API
    doc["id"] = str(doc.pop("_id"))

    # Muy importante: facultad_id como string (no ObjectId crudo)
    if "facultad_id" in doc and not isinstance(doc["facultad_id"], str):
        doc["facultad_id"] = str(doc["facultad_id"])

    return ProgramaAcademicoOut(**doc)


async def create_programa_academico_crud(
    data: ProgramaAcademicoCreate,
) -> ProgramaAcademicoOut:
    payload = data.model_dump()
    result = await collection.insert_one(payload)
    new_doc = await collection.find_one({"_id": result.inserted_id})
    return _to_out(new_doc)


async def list_programa_academicos_crud() -> List[ProgramaAcademicoOut]:
    docs: List[ProgramaAcademicoOut] = []
    cursor = collection.find({})

    async for d in cursor:
        docs.append(_to_out(d))

    return docs


async def get_programa_academico_crud(id: str) -> ProgramaAcademicoOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Programa académico no encontrado",
        )

    return _to_out(doc)


async def update_programa_academico_crud(
    id: str, data: ProgramaAcademicoUpdate
) -> ProgramaAcademicoOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    update_data = {
        k: v for k, v in data.model_dump(exclude_unset=True).items()
    }

    # Si no hay datos para actualizar, devolvemos el documento actual
    if not update_data:
        doc = await collection.find_one({"_id": oid})
        if not doc:
            raise HTTPException(
                status_code=404,
                detail="Programa académico no encontrado",
            )
        return _to_out(doc)

    result = await collection.update_one({"_id": oid}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Programa académico no encontrado",
        )

    doc = await collection.find_one({"_id": oid})
    return _to_out(doc)


async def delete_programa_academico_crud(id: str) -> dict:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await collection.delete_one({"_id": oid})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Programa académico no encontrado",
        )

    return {"msg": "Programa académico eliminado"}
