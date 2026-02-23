from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.enums import FinalizeStatus, Status


class InspectionBase(BaseModel):
    establishment_id: int
    date_time: Optional[datetime] = None
    status: Status = Status.clear


class InspectionCreate(InspectionBase):
    pass


class InspectionCreateService(InspectionBase):
    inspector_id: int


class InspectionUpdate(BaseModel):
    establishment_id: Optional[int] = None
    status: Optional[Status] = None


class InspectionResponse(InspectionBase):
    id: int
    created_at: datetime
    inspector_id: int

    class Config:
        from_attributes = True


class LogResponse(BaseModel):
    id: int
    inspection_id: int
    old_status: Status
    new_status: Status
    date_time: datetime

    class Config:
        from_attributes = True


class FinalizeInspection(BaseModel):
    inspection_id: int
    status: FinalizeStatus
    pending_issues: str


class FinalizeInspectionService(FinalizeInspection):
    inspector_id: int


class FinalizeInspectionResponse(FinalizeInspectionService):
    id: int

    class Config:
        from_attributes = True
