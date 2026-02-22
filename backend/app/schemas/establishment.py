from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EstablishmentBase(BaseModel):
    name: str
    address: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None


class EstablishmentCreate(EstablishmentBase):
    pass


class EstablishmentUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None


class EstablishmentResponse(EstablishmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
