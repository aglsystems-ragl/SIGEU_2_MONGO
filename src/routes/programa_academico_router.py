from fastapi import APIRouter, status
from typing import List
from src.models.programa_academico import ProgramaAcademicoCreate, ProgramaAcademicoOut, ProgramaAcademicoUpdate
from src.crud.programa_academico_crud import (
    create_programa_academico_crud,
    list_programa_academicos_crud,
    get_programa_academico_crud,
    update_programa_academico_crud,
    delete_programa_academico_crud,
)

router = APIRouter(prefix="/programa_academicos", tags=["Programas académicos"])

@router.post("/", response_model=ProgramaAcademicoOut, status_code=status.HTTP_201_CREATED)
async def create_programa_academico_endpoint(payload: ProgramaAcademicoCreate):
    return await create_programa_academico_crud(payload)

@router.get("/", response_model=List[ProgramaAcademicoOut])
async def list_programa_academicos_endpoint():
    return await list_programa_academicos_crud()

@router.get("/{item_id}", response_model=ProgramaAcademicoOut)
async def get_programa_academico_endpoint(item_id: str):
    return await get_programa_academico_crud(item_id)

@router.put("/{item_id}", response_model=ProgramaAcademicoOut)
async def update_programa_academico_endpoint(item_id: str, payload: ProgramaAcademicoUpdate):
    return await update_programa_academico_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_programa_academico_endpoint(item_id: str):
    return await delete_programa_academico_crud(item_id)
