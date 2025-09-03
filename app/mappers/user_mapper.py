from typing import Optional
from app.entities.user import UserEntity
from app.dtos.user_dto import UserDto,UserOutDto,UserUpdateDto


class UserMapper:
    @staticmethod
    def to_out_dto(user: UserEntity) -> UserOutDto:
        return UserOutDto.model_validate(user)

    @staticmethod
    def from_create_dto(dto: UserDto, password_hash: str) -> UserEntity:
        return UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash
        )

    @staticmethod
    def apply_update(entity: UserEntity, dto: UserUpdateDto) -> UserEntity:
        if dto.name is not None:
            entity.name = dto.name
        if dto.email is not None:
            entity.email = dto.email
        return entity