from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.Base import Base

class Application(Base):
    __tablename__ = 'application'
    id: Mapped[int] = mapped_column(primary_key=True)
    application_name: Mapped[str] = mapped_column(String(255), unique=True)

    # Relationship with usage table
    usage: Mapped[List["Usage"]] = relationship(back_populates="application")
