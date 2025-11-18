from fastapi import APIRouter, status
from typing import List
from src.models.unidad_academica import UnidadAcademicaCreate, UnidadAcademicaOut, UnidadAcademicaUpdate
from src.crud.unidad_academica_crud import (
    create_unidad_academica_crud,
    list_unidad_academicas_crud,
    get_unidad_academica_crud,
    update_unidad_academica_crud,
    delete_unidad_academica_crud,
)

router = APIRouter(prefix="/unidad_academicas", tags=["Unidades académicas"])

@router.post("/", response_model=UnidadAcademicaOut, status_code=status.HTTP_201_CREATED)
async def create_unidad_academica_endpoint(payload: UnidadAcademicaCreate):
    return await create_unidad_academica_crud(payload)

@router.get("/", response_model=List[UnidadAcademicaOut])
async def list_unidad_academicas_endpoint():
    return await list_unidad_academicas_crud()

@router.get("/{item_id}", response_model=UnidadAcademicaOut)
async def get_unidad_academica_endpoint(item_id: str):
    return await get_unidad_academica_crud(item_id)

@router.put("/{item_id}", response_model=UnidadAcademicaOut)
async def update_unidad_academica_endpoint(item_id: str, payload: UnidadAcademicaUpdate):
    return await update_unidad_academica_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_unidad_academica_endpoint(item_id: str):
    return await delete_unidad_academica_crud(item_id)
