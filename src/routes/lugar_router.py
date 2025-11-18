from fastapi import APIRouter, status
from typing import List
from src.models.lugar import LugarCreate, LugarOut, LugarUpdate
from src.crud.lugar_crud import (
    create_lugar_crud,
    list_lugars_crud,
    get_lugar_crud,
    update_lugar_crud,
    delete_lugar_crud,
)

router = APIRouter(prefix="/lugars", tags=["Lugares"])

@router.post("/", response_model=LugarOut, status_code=status.HTTP_201_CREATED)
async def create_lugar_endpoint(payload: LugarCreate):
    return await create_lugar_crud(payload)

@router.get("/", response_model=List[LugarOut])
async def list_lugars_endpoint():
    return await list_lugars_crud()

@router.get("/{item_id}", response_model=LugarOut)
async def get_lugar_endpoint(item_id: str):
    return await get_lugar_crud(item_id)

@router.put("/{item_id}", response_model=LugarOut)
async def update_lugar_endpoint(item_id: str, payload: LugarUpdate):
    return await update_lugar_crud(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_lugar_endpoint(item_id: str):
    return await delete_lugar_crud(item_id)
