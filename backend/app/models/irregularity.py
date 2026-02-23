import datetime
from app.enums import Severity
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.decorators import IntEnum


class Irregularities(Base):
    __tablename__ = "irregularities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inspection_id: Mapped[int] = mapped_column(Integer, ForeignKey("inspections.id"))
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    severity: Mapped[int] = mapped_column(IntEnum(Severity), default=Severity.moderate)
    requires_interruption: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
