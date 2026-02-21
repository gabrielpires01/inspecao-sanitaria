from app.enums import RoleEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.inspector)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
