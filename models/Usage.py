import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from models.Base import Base

class Usage(Base):
    __tablename__ = 'usage'

    id: Mapped[int] = mapped_column(primary_key=True)
    seconds: Mapped[int]
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship with application table
    application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
    application: Mapped["Application"] = relationship(back_populates="usage")
