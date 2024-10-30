from __future__ import annotations

from datetime import datetime
from typing import List
from sqlalchemy import Integer, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

user_presentation = Table(
    "user_presentation",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("presentation_id", Integer, ForeignKey("presentation.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str]
    presentations: Mapped[List[Presentation]] = relationship(secondary=user_presentation,  back_populates="users")

class Presentation(Base):
    __tablename__ = "presentation"

    title: Mapped[str] = mapped_column(unique=True)
    users: Mapped[List[User]] = relationship(secondary=user_presentation,  back_populates="presentations")

class Room(Base):
    __tablename__ = "room"

    name: Mapped[str]

class Schedule(Base):
    __tablename__ = "schedule"

    presentation_id: Mapped[int] = mapped_column(ForeignKey("presentation.id"))
    presentation: Mapped["Presentation"] = relationship()

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped["Room"] = relationship()

    date_time: Mapped[datetime]