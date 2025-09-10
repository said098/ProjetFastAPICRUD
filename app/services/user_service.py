# app/services/user_service.py
from typing import List, Optional
from uuid import UUID
from passlib.context import CryptContext

from app.interfaces.user_interface import InterfaceUserService
from app.repositories.user_repository import UserRepository
from app.dtos.user_dto import UserDto, UserUpdateDto, UserOutDto
from app.mappers.user_mapper import UserMapper

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(InterfaceUserService):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self) -> List[UserOutDto]:
        users = self.repository.get_all()
        return [UserMapper.to_out_dto(u) for u in users]

    def get_user_by_id(self, user_id: UUID) -> Optional[UserOutDto]:
        user = self.repository.get_by_id(user_id)
        return UserMapper.to_out_dto(user) if user else None

    def create_user(self, user_dto: UserDto) -> UserOutDto:
        if self.repository.get_by_email(user_dto.email):
            raise ValueError("Email déjà enregistré")
        password_hash = pwd.hash(user_dto.password)
        entity = UserMapper.from_create_dto(user_dto, password_hash)
        created = self.repository.create(entity)
        return UserMapper.to_out_dto(created)

    def update_user(self, user_id: UUID, user_dto: UserUpdateDto) -> Optional[UserOutDto]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        if user_dto.email is not None:
            existing = self.repository.get_by_email(user_dto.email)
            if existing and existing.id != user.id:
                raise ValueError("Email déjà enregistré")

        UserMapper.apply_update(user, user_dto)
        if getattr(user_dto, "password", None):
            user.password = pwd.hash(user_dto.password)

        updated = self.repository.update(user)
        return UserMapper.to_out_dto(updated)

    def delete_user(self, user_id: UUID) -> bool:
        return self.repository.delete(user_id) is not None
