from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.db.database import Base
from typing import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    events: Mapped[List["Event"]] = relationship("Event", backref="user", cascade= "all, delete-orphan", lazy='joined' )
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", backref="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", backref="user", cascade="all, delete-orphan")

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str] = mapped_column(Text)
    capacity: Mapped[int] = mapped_column(Integer, default=10)
    content: Mapped[JSONB] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", backref="events", cascade="all, delete-orphan")

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    num_guests: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[JSONB] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id", ondelete="CASCADE", onupdate="CASCADE"))

