import datetime
from app.enums import Status
from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base


class Establishments(Base):
    __tablename__ = "establishments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    cep: Mapped[str] = mapped_column(String(9), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Inspections(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    establishment_id: Mapped[int] = mapped_column(Integer, ForeignKey("establishments.id"))
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[int] = mapped_column(Enum(Status), default=Status.authorized)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
