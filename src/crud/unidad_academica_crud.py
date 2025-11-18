from bson import ObjectId
from fastapi import HTTPException
from typing import List
from src.db.client import db
from src.models.unidad_academica import UnidadAcademicaCreate, UnidadAcademicaOut, UnidadAcademicaUpdate

collection = db["unidad_academica"]

def _to_out(doc) -> UnidadAcademicaOut:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return UnidadAcademicaOut(**doc)

async def create_unidad_academica_crud(data: UnidadAcademicaCreate) -> UnidadAcademicaOut:
    payload = data.model_dump()
    result = await collection.insert_one(payload)
    doc = await collection.find_one({"_id": result.inserted_id})
    return _to_out(doc)

async def list_unidad_academicas_crud() -> List[UnidadAcademicaOut]:
    docs = []
    async for d in collection.find():
        docs.append(_to_out(d))
    return docs

async def get_unidad_academica_crud(id: str) -> UnidadAcademicaOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Unidad académica no encontrado")
    return _to_out(doc)

async def update_unidad_academica_crud(id: str, data: UnidadAcademicaUpdate) -> UnidadAcademicaOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    update_data = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
    if not update_data:
        doc = await collection.find_one({"_id": oid})
        if not doc:
            raise HTTPException(status_code=404, detail="Unidad académica no encontrado")
        return _to_out(doc)

    result = await collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Unidad académica no encontrado")

    doc = await collection.find_one({"_id": oid})
    return _to_out(doc)

async def delete_unidad_academica_crud(id: str) -> dict:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Unidad académica no encontrado")
    return {"msg": "Unidad académica eliminado"}
