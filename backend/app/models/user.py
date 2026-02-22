from datetime import datetime
from app.enums import RoleEnum
from app.core.decorators import IntEnum
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[int] = mapped_column(IntEnum(RoleEnum), default=RoleEnum.inspector)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
