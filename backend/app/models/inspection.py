from app.enums import Status
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Establishments(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(String(255), nullable=True)
    cep = Column(String(9), nullable=True)
    city = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Inspections(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    establishment_id = Column(Integer, ForeignKey("establishments.id"))
    inspector_id = Column(Integer, ForeignKey("users.id"))
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Status), default=Status.authorized)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
