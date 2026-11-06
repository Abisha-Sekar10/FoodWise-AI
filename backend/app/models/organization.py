from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # College Cafeteria, Hospital, Corporate Canteen, Hotel
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, default="New Delhi")
    state = Column(String(100), nullable=False, default="Delhi")
    latitude = Column(Float, nullable=False, default=28.6139)
    longitude = Column(Float, nullable=False, default=77.2090)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=False)
    fssai_license = Column(String(100), nullable=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="institution", foreign_keys="User.institution_id")
    kitchens = relationship("Kitchen", back_populates="institution", cascade="all, delete-orphan")

class Kitchen(Base):
    __tablename__ = "kitchens"

    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    daily_capacity_meals = Column(Integer, default=500)
    service_type = Column(String(100), default="Buffet & Meal Trays")  # Buffet, Thali, Ala Carte
    storage_capacity_kg = Column(Float, default=1000.0)
    has_cold_storage = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    institution = relationship("Institution", back_populates="kitchens")
    users = relationship("User", back_populates="kitchen", foreign_keys="User.kitchen_id")
    inventory = relationship("FoodInventory", back_populates="kitchen", cascade="all, delete-orphan")
    productions = relationship("FoodProduction", back_populates="kitchen", cascade="all, delete-orphan")
    consumptions = relationship("FoodConsumption", back_populates="kitchen", cascade="all, delete-orphan")
    predictions = relationship("DemandPrediction", back_populates="kitchen", cascade="all, delete-orphan")
    surpluses = relationship("FoodSurplus", back_populates="kitchen", cascade="all, delete-orphan")
    iot_sensors = relationship("IoTSensorReading", back_populates="kitchen", cascade="all, delete-orphan")
    donations = relationship("FoodDonation", back_populates="kitchen", cascade="all, delete-orphan")

class FoodProcessingUnit(Base):
    __tablename__ = "food_processing_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False)  # Dairy Processing, Grain Milling, Fruit & Veg Canning, Bakery
    location = Column(String(255), nullable=False)
    daily_processing_capacity_tons = Column(Float, default=10.0)
    latitude = Column(Float, nullable=False, default=28.5355)
    longitude = Column(Float, nullable=False, default=77.3910)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="processing_unit", foreign_keys="User.processing_unit_id")
    records = relationship("ProductionRecord", back_populates="unit", cascade="all, delete-orphan")
    machines = relationship("MachineMonitoring", back_populates="unit", cascade="all, delete-orphan")
    energy_logs = relationship("EnergyConsumption", back_populates="unit", cascade="all, delete-orphan")

class NGO(Base):
    __tablename__ = "ngos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(100), nullable=False)  # NGO Darpan / 80G
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, default="New Delhi")
    latitude = Column(Float, nullable=False, default=28.6289)
    longitude = Column(Float, nullable=False, default=77.2065)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=False)
    daily_meals_capacity = Column(Integer, default=300)
    preferred_food_categories = Column(String(255), default="Cooked Meals, Breads, Fruits, Packaged Foods")
    has_refrigerated_transport = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="ngo", foreign_keys="User.ngo_id")
    donations = relationship("FoodDonation", back_populates="accepted_ngo")
    requests = relationship("DonationRequest", back_populates="ngo", cascade="all, delete-orphan")
