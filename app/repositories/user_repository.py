# app/repositories/user_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.entities.user import UserEntity
from app.repositories.general_repository import GeneralRepository

class UserRepository(GeneralRepository[UserEntity]):
    def __init__(self, session: Session):
        super().__init__(session=session, model=UserEntity)

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        stmt = select(UserEntity).where(UserEntity.email == email)
        return self.session.scalars(stmt).first()


"""
class UserRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        stmt = (
            select(UserEntity)
            .order_by(UserEntity.id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt))

    def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        return self.db.get(UserEntity, user_id)

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        stmt = select(UserEntity).where(UserEntity.email == email)
        return self.db.scalars(stmt).first()

    # CREATE
    def create(self, entity: UserEntity) -> UserEntity:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # UPDATE
    def update(self, entity: UserEntity) -> UserEntity:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # DELETE
    def delete(self, entity: UserEntity) -> None:
        self.db.delete(entity)
        self.db.commit()
"""