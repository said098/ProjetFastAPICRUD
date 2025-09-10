# app/controllers/user_controller.py
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from app.dependencies.dependencies import get_user_service
from app.interfaces.user_interface import InterfaceUserService
from app.dtos.user_dto import UserDto, UserUpdateDto, UserOutDto

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOutDto])
def list_users(service: InterfaceUserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserOutDto)
def get_user(user_id: UUID, service: InterfaceUserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserOutDto, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserDto, service: InterfaceUserService = Depends(get_user_service)):
    try:
        return service.create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.put("/{user_id}", response_model=UserOutDto)
def update_user(user_id: UUID, payload: UserUpdateDto, service: InterfaceUserService = Depends(get_user_service)):
    try:
        updated = service.update_user(user_id, payload)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, service: InterfaceUserService = Depends(get_user_service)):
    ok = service.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse({"deleted": True, "id": str(user_id)}, status_code=200)
