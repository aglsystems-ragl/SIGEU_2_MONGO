from bson import ObjectId
from fastapi import HTTPException
from typing import List
from src.db.client import db
from src.models.lugar import LugarCreate, LugarOut, LugarUpdate

collection = db["lugar"]

def _to_out(doc) -> LugarOut:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return LugarOut(**doc)

async def create_lugar_crud(data: LugarCreate) -> LugarOut:
    payload = data.model_dump()
    result = await collection.insert_one(payload)
    doc = await collection.find_one({"_id": result.inserted_id})
    return _to_out(doc)

async def list_lugars_crud() -> List[LugarOut]:
    docs = []
    async for d in collection.find():
        docs.append(_to_out(d))
    return docs

async def get_lugar_crud(id: str) -> LugarOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return _to_out(doc)

async def update_lugar_crud(id: str, data: LugarUpdate) -> LugarOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    update_data = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
    if not update_data:
        doc = await collection.find_one({"_id": oid})
        if not doc:
            raise HTTPException(status_code=404, detail="Lugar no encontrado")
        return _to_out(doc)

    result = await collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    doc = await collection.find_one({"_id": oid})
    return _to_out(doc)

async def delete_lugar_crud(id: str) -> dict:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return {"msg": "Lugar eliminado"}
