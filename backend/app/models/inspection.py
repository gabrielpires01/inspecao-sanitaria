from datetime import datetime
from app.enums import FinalizeStatus, Status
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.decorators import IntEnum


class Establishments(Base):
    __tablename__ = "establishments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    cep: Mapped[str] = mapped_column(String(9), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Inspections(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    establishment_id: Mapped[int] = mapped_column(Integer, ForeignKey("establishments.id"))
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[int] = mapped_column(IntEnum(Status), default=Status.clear)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class InspectionLog(Base):
    __tablename__ = "inspection_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inspection_id: Mapped[int] = mapped_column(Integer, ForeignKey("inspections.id"))
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    old_status: Mapped[int] = mapped_column(IntEnum(Status), default=Status.clear)
    new_status: Mapped[int] = mapped_column(IntEnum(Status), default=Status.clear)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())


class FinalizationLog(Base):
    __tablename__ = "finalization_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inspection_id: Mapped[int] = mapped_column(Integer, ForeignKey("inspections.id"))
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[int] = mapped_column(IntEnum(FinalizeStatus), default=Status.clear)
    pending_issues: Mapped[str] = mapped_column(String(255), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
