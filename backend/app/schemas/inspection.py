from app.enums import Status
from pydantic import BaseModel
from datetime import datetime


class InspectionUpdate(BaseModel):
    status: Status


class InspectionCreate(BaseModel):
    establishment_id: int
    inspector_id: int
    data_time: datetime
