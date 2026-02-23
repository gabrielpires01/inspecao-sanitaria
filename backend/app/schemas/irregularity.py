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
    description: Optional[str] = None
    severity: Optional[Severity] = None


class IrregularityUpdateSchema(BaseModel):
    description: Optional[str] = None
    severity: Optional[Severity] = None
    inspector_id: int


class IrregularityResponse(IrregularityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class IrregularityResolve(BaseModel):
    description: str


class IrregularityLogsResponse(BaseModel):
    id: int
    irregularity_id: int
    inspector_id: int
    old_severity: int
    new_severity: int
    created_at: datetime
