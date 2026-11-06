from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProductionRecord(Base):
    __tablename__ = "production_records"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("food_processing_units.id", ondelete="CASCADE"), nullable=False)
    batch_number = Column(String(100), unique=True, index=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    date = Column(Date, default=date.today)
    raw_material_input_kg = Column(Float, nullable=False)
    finished_product_output_kg = Column(Float, nullable=False)
    material_loss_kg = Column(Float, nullable=False)
    production_efficiency_pct = Column(Float, nullable=False)  # (Output / Input) * 100
    planned_production_kg = Column(Float, nullable=False)
    variance_pct = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    unit = relationship("FoodProcessingUnit", back_populates="records")

class MachineMonitoring(Base):
    __tablename__ = "machine_monitoring"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("food_processing_units.id", ondelete="CASCADE"), nullable=False)
    machine_name = Column(String(255), nullable=False)
    machine_code = Column(String(50), nullable=False)  # e.g., EXTRUDER-01, PASTEURIZER-02, RETORT-01
    status = Column(String(50), default="OPERATIONAL")  # OPERATIONAL, MAINTENANCE, DOWNTIME, WARNING
    operating_hours = Column(Float, default=8.0)
    downtime_minutes = Column(Float, default=0.0)
    downtime_reason = Column(String(255), nullable=True)
    temperature_celsius = Column(Float, default=75.0)
    vibration_mm_s = Column(Float, default=1.2)
    pressure_bar = Column(Float, default=3.5)
    maintenance_due_date = Column(Date, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    unit = relationship("FoodProcessingUnit", back_populates="machines")

class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("food_processing_units.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, default=date.today)
    shift = Column(String(50), default="Morning Shift")  # Morning, Afternoon, Night
    electricity_kwh = Column(Float, nullable=False)
    water_liters = Column(Float, nullable=False)
    fuel_liters = Column(Float, default=0.0)
    specific_energy_kwh_per_kg = Column(Float, nullable=False)  # kWh / kg produced
    is_abnormal_consumption = Column(Boolean, default=False)
    alert_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    unit = relationship("FoodProcessingUnit", back_populates="energy_logs")
