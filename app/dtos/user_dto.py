from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# --- Entrée (creation) ---
class UserDto(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=6)

# --- Entrée (update partiel) ---
class UserUpdateDto(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6)

# --- Sortie (lecture) ---
class UserOutDto(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True   # Pydantic v2
