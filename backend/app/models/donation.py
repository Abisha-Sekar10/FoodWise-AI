import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class DonationStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ACCEPTED = "ACCEPTED"
    PICKUP_SCHEDULED = "PICKUP_SCHEDULED"
    COLLECTED = "COLLECTED"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class FoodDonation(Base):
    __tablename__ = "food_donations"

    id = Column(Integer, primary_key=True, index=True)
    donation_code = Column(String(50), unique=True, index=True, nullable=False)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    surplus_id = Column(Integer, ForeignKey("food_surplus.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(255), nullable=False)
    food_category = Column(String(100), nullable=False)  # Cooked Meals, Bakery, Fresh Produce, Packaged Food
    quantity_kg = Column(Float, nullable=False)
    portions = Column(Integer, nullable=False)
    preparation_time = Column(DateTime, nullable=False)
    safe_use_deadline = Column(DateTime, nullable=False)  # Expiry deadline for redistribution
    storage_condition = Column(String(100), default="Heated Container / Hot Holding (>60°C)")
    packaging_type = Column(String(100), default="Food-grade Insulated Cans")
    
    pickup_address = Column(Text, nullable=False)
    pickup_latitude = Column(Float, nullable=False)
    pickup_longitude = Column(Float, nullable=False)
    special_instructions = Column(Text, nullable=True)
    
    status = Column(Enum(DonationStatus), default=DonationStatus.AVAILABLE, nullable=False, index=True)
    safety_verified = Column(Boolean, default=True)  # verified food safety requirements
    
    accepted_ngo_id = Column(Integer, ForeignKey("ngos.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    kitchen = relationship("Kitchen", back_populates="donations")
    surplus_record = relationship("FoodSurplus", back_populates="donation")
    accepted_ngo = relationship("NGO", back_populates="donations")
    requests = relationship("DonationRequest", back_populates="donation", cascade="all, delete-orphan")
    pickup_schedule = relationship("PickupSchedule", back_populates="donation", uselist=False, cascade="all, delete-orphan")
    tracking = relationship("DeliveryTracking", back_populates="donation", uselist=False, cascade="all, delete-orphan")

class DonationRequest(Base):
    __tablename__ = "donation_requests"

    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("food_donations.id", ondelete="CASCADE"), nullable=False)
    ngo_id = Column(Integer, ForeignKey("ngos.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="PENDING")  # PENDING, ACCEPTED, REJECTED, EXPIRED
    estimated_arrival_minutes = Column(Integer, default=30)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    donation = relationship("FoodDonation", back_populates="requests")
    ngo = relationship("NGO", back_populates="requests")

class PickupSchedule(Base):
    __tablename__ = "pickup_schedules"

    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("food_donations.id", ondelete="CASCADE"), nullable=False, unique=True)
    vehicle_type = Column(String(100), default="Refrigerated Van")  # Van, Electric Cargo Bike, Light Truck
    driver_name = Column(String(255), default="Volunteer Team Alpha")
    driver_phone = Column(String(50), default="+91 98765 43210")
    scheduled_pickup_time = Column(DateTime, nullable=False)
    estimated_delivery_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    donation = relationship("FoodDonation", back_populates="pickup_schedule")

class DeliveryTracking(Base):
    __tablename__ = "delivery_tracking"

    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("food_donations.id", ondelete="CASCADE"), nullable=False, unique=True)
    current_status = Column(Enum(DonationStatus), default=DonationStatus.AVAILABLE)
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    route_waypoints = Column(JSON, nullable=True)  # List of coordinates [[lat, lng], ...]
    eta_minutes = Column(Integer, default=25)
    distance_remaining_km = Column(Float, default=5.2)
    temperature_logged_celsius = Column(Float, default=4.0)  # Cold chain verification during transit
    delivered_at = Column(DateTime, nullable=True)
    receiver_signature_name = Column(String(255), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    donation = relationship("FoodDonation", back_populates="tracking")
