from fastapi import APIRouter, status
from typing import List
from src.models.facultad import FacultadCreate, FacultadOut, FacultadUpdate
from src.crud.facultad_crud import (
    create_facultad_crud,
    list_facultads_crud,
    get_facultad_crud,
    update_facultad_crud,
    delete_facultad_crud,
)

router = APIRouter(prefix="/facultads", tags=["Facultades"])

@router.post("/", response_model=FacultadOut, status_code=status.HTTP_201_CREATED)
async def create_facultad_endpoint(payload: FacultadCreate):
    return await create_facultad_crud(payload)

@router.get("/", response_model=List[FacultadOut])
async def list_facultads_endpoint():
    return await list_facultads_crud()

@router.get("/{item_id}", response_model=FacultadOut)
async def get_facultad_endpoint(item_id: str):
    return await get_facultad_crud(item_id)

@router.put("/{item_id}", response_model=FacultadOut)
async def update_facultad_endpoint(item_id: str, payload: FacultadUpdate):
    return await update_facultad_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_facultad_endpoint(item_id: str):
    return await delete_facultad_crud(item_id)
