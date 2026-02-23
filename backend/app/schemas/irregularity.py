from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.enums import Severity


class IrregularityBase(BaseModel):
    inspection_id: int
    description: str
    severity: Severity = Severity.moderate
    requires_interruption: bool = False


class IrregularityCreate(IrregularityBase):
    pass


class IrregularityCreateSchema(IrregularityBase):
    inspector_id: int


class IrregularityUpdate(BaseModel):
    description: Optional[int] = None
    severity: Optional[Severity] = None


class IrregularityResponse(IrregularityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
