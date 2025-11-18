from fastapi import APIRouter, status
from typing import List
from src.models.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate
from src.crud.usuario_crud import (
    create_usuario_crud,
    list_usuarios_crud,
    get_usuario_crud,
    update_usuario_crud,
    delete_usuario_crud,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def create_usuario_endpoint(payload: UsuarioCreate):
    return await create_usuario_crud(payload)

@router.get("/", response_model=List[UsuarioOut])
async def list_usuarios_endpoint():
    return await list_usuarios_crud()

@router.get("/{item_id}", response_model=UsuarioOut)
async def get_usuario_endpoint(item_id: str):
    return await get_usuario_crud(item_id)

@router.put("/{item_id}", response_model=UsuarioOut)
async def update_usuario_endpoint(item_id: str, payload: UsuarioUpdate):
    return await update_usuario_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_usuario_endpoint(item_id: str):
    return await delete_usuario_crud(item_id)
