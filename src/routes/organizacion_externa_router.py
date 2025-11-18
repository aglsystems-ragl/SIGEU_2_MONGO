from fastapi import APIRouter, status
from typing import List
from src.models.organizacion_externa import OrganizacionExternaCreate, OrganizacionExternaOut, OrganizacionExternaUpdate
from src.crud.organizacion_externa_crud import (
    create_organizacion_externa_crud,
    list_organizacion_externas_crud,
    get_organizacion_externa_crud,
    update_organizacion_externa_crud,
    delete_organizacion_externa_crud,
)

router = APIRouter(prefix="/organizacion_externas", tags=["Organizaciones externas"])

@router.post("/", response_model=OrganizacionExternaOut, status_code=status.HTTP_201_CREATED)
async def create_organizacion_externa_endpoint(payload: OrganizacionExternaCreate):
    return await create_organizacion_externa_crud(payload)

@router.get("/", response_model=List[OrganizacionExternaOut])
async def list_organizacion_externas_endpoint():
    return await list_organizacion_externas_crud()

@router.get("/{item_id}", response_model=OrganizacionExternaOut)
async def get_organizacion_externa_endpoint(item_id: str):
    return await get_organizacion_externa_crud(item_id)

@router.put("/{item_id}", response_model=OrganizacionExternaOut)
async def update_organizacion_externa_endpoint(item_id: str, payload: OrganizacionExternaUpdate):
    return await update_organizacion_externa_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_organizacion_externa_endpoint(item_id: str):
    return await delete_organizacion_externa_crud(item_id)
