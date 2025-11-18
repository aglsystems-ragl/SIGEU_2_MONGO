from fastapi import APIRouter, status
from typing import List
from src.models.evento import EventoCreate, EventoOut, EventoUpdate
from src.crud.evento_crud import (
    create_evento_crud,
    list_eventos_crud,
    get_evento_crud,
    update_evento_crud,
    delete_evento_crud,
)

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("/", response_model=EventoOut, status_code=status.HTTP_201_CREATED)
async def create_evento_endpoint(payload: EventoCreate):
    return await create_evento_crud(payload)

@router.get("/", response_model=List[EventoOut])
async def list_eventos_endpoint():
    return await list_eventos_crud()

@router.get("/{item_id}", response_model=EventoOut)
async def get_evento_endpoint(item_id: str):
    return await get_evento_crud(item_id)

@router.put("/{item_id}", response_model=EventoOut)
async def update_evento_endpoint(item_id: str, payload: EventoUpdate):
    return await update_evento_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_evento_endpoint(item_id: str):
    return await delete_evento_crud(item_id)
