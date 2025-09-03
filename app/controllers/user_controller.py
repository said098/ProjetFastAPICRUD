from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.connection_db.database_connnection import get_db
from app.services.user_service import UserService
from app.dtos.user_dto import UserDto, UserUpdateDto, UserOutDto

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOutDto])
def list_users(db: Session = Depends(get_db)):
    return UserService(db).get_all_users()


@router.get("/{user_id}", response_model=UserOutDto)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserService(db).get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=UserOutDto)
def create_user(user: UserDto, db: Session = Depends(get_db)):
    user = UserService(db).create_user(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not created")
    return user