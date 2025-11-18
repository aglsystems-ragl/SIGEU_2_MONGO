from bson import ObjectId
from fastapi import HTTPException
from typing import List
from src.db.client import db
from src.models.organizacion_externa import OrganizacionExternaCreate, OrganizacionExternaOut, OrganizacionExternaUpdate

collection = db["organizacion_externa"]

def _to_out(doc) -> OrganizacionExternaOut:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return OrganizacionExternaOut(**doc)

async def create_organizacion_externa_crud(data: OrganizacionExternaCreate) -> OrganizacionExternaOut:
    payload = data.model_dump()
    result = await collection.insert_one(payload)
    doc = await collection.find_one({"_id": result.inserted_id})
    return _to_out(doc)

async def list_organizacion_externas_crud() -> List[OrganizacionExternaOut]:
    docs = []
    async for d in collection.find():
        docs.append(_to_out(d))
    return docs

async def get_organizacion_externa_crud(id: str) -> OrganizacionExternaOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Organización externa no encontrado")
    return _to_out(doc)

async def update_organizacion_externa_crud(id: str, data: OrganizacionExternaUpdate) -> OrganizacionExternaOut:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    update_data = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
    if not update_data:
        doc = await collection.find_one({"_id": oid})
        if not doc:
            raise HTTPException(status_code=404, detail="Organización externa no encontrado")
        return _to_out(doc)

    result = await collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Organización externa no encontrado")

    doc = await collection.find_one({"_id": oid})
    return _to_out(doc)

async def delete_organizacion_externa_crud(id: str) -> dict:
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Organización externa no encontrado")
    return {"msg": "Organización externa eliminado"}
