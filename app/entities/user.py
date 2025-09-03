from sqlalchemy import Column, Integer, String, Boolean
from app.connection_db.database_connnection import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserEntity(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    email = Column(String(255),unique=True,nullable=False)
    password = Column(String(255),nullable=False)

