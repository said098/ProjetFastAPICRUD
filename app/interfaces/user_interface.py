from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.dtos.user_dto import UserDto


# app/interfaces/i_user_service.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.dtos.user_dto import UserDto, UserUpdateDto, UserOutDto

class InterfaceUserService(ABC):
    @abstractmethod
    def get_all_users(self) -> List[UserOutDto]:
        ...

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[UserOutDto]:
        ...

    @abstractmethod
    def create_user(self, user_dto: UserDto) -> UserOutDto:
        ...

    @abstractmethod
    def update_user(self, user_id: UUID, user_dto: UserUpdateDto) -> Optional[UserOutDto]:
        ...

    @abstractmethod
    def delete_user(self, user_id: UUID) -> bool:
        ...
