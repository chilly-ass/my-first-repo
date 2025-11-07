from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class RegistrationStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Platform(str, enum.Enum):
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True, index=True)
    whatsapp_phone = Column(String, unique=True, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    registrations = relationship("EventRegistration", back_populates="user", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False, index=True)
    location = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")


class EventRegistration(Base):
    __tablename__ = "event_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registered_via = Column(String, nullable=False)
    status = Column(String, nullable=False, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")


class UserState(Base):
    __tablename__ = "user_states"
    
    id = Column(Integer, primary_key=True, index=True)
    user_platform_id = Column(String, unique=True, nullable=False, index=True)
    platform = Column(String, nullable=False)
    current_state = Column(String, nullable=True)
    state_data = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
