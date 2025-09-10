# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.connection_db.database_connnection import get_db
from app.repositories.user_repository import UserRepository
from app.interfaces.user_interface import InterfaceUserService
from app.services.user_service import UserService

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> InterfaceUserService:
    return UserService(repo)
