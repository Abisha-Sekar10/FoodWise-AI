import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    KITCHEN_MANAGER = "KITCHEN_MANAGER"
    PROCESSING_MANAGER = "PROCESSING_MANAGER"
    NGO = "NGO"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.KITCHEN_MANAGER)
    phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Keys to associated entity (depending on role)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="SET NULL"), nullable=True)
    processing_unit_id = Column(Integer, ForeignKey("food_processing_units.id", ondelete="SET NULL"), nullable=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    institution = relationship("Institution", back_populates="users", foreign_keys=[institution_id])
    kitchen = relationship("Kitchen", back_populates="users", foreign_keys=[kitchen_id])
    processing_unit = relationship("FoodProcessingUnit", back_populates="users", foreign_keys=[processing_unit_id])
    ngo = relationship("NGO", back_populates="users", foreign_keys=[ngo_id])
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
