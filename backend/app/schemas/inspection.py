from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.enums import Status


class InspectionBase(BaseModel):
    establishment_id: int
    inspector_id: int
    date_time: Optional[datetime] = None
    status: Status = Status.authorized


class InspectionCreate(InspectionBase):
    pass


class InspectionUpdate(BaseModel):
    establishment_id: Optional[int] = None
    inspector_id: Optional[int] = None
    status: Optional[Status] = None


class InspectionResponse(InspectionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
