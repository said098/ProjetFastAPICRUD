from typing import List,Optional
from uuid import UUID
from passlib.context import CryptContext
from sqlalchemy.orm  import Session

from app.repositories.user_repository import UserRepository
from app.dtos.user_dto import UserDto, UserUpdateDto, UserOutDto   # tes DTOs
from app.mappers.user_mapper import UserMapper

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    # READ ALL
    def get_all_users(self) -> List[UserOutDto]:
        users = self.repository.get_all()
        return [UserMapper.to_out_dto(u) for u in users]

    # READ ONE
    def get_user_by_id(self, user_id: UUID) -> Optional[UserOutDto]:
        user = self.repository.get_by_id(user_id)
        return UserMapper.to_out_dto(user) if user else None

    # CREATE
    def create_user(self, user_dto: UserDto) -> UserOutDto:
        # email unique
        if self.repository.get_by_email(user_dto.email):
            raise ValueError("Email déja enregistré")
        password_hash = pwd.hash(user_dto.password)
        user = UserMapper.from_create_dto(user_dto, password_hash=password_hash)
        created = self.repository.create(user)
        return UserMapper.to_out_dto(created)

    # UPDATE
    def update_user(self, user_id: UUID, user_dto: UserUpdateDto) -> Optional[UserOutDto]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        if user_dto.email is not None:
            existing = self.repository.get_by_email(user_dto.email)
            if existing and existing.id != user.id:
                raise ValueError("Email déja enregistré")
        UserMapper.apply_update(user, user_dto)

        # hash si password présent
        if getattr(user_dto, "password", None):
            user.password = pwd.hash(user_dto.password)

        updated = self.repository.update(user)
        return UserMapper.to_out_dto(updated)

    # DELETE
    def delete_user(self, user_id: UUID) -> bool:
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        self.repository.delete(user)
        return True