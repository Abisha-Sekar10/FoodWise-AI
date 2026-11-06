from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class WasteAnalytics(Base):
    __tablename__ = "waste_analytics"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)  # KITCHEN, PROCESSING_UNIT
    entity_id = Column(Integer, nullable=False, index=True)
    date = Column(Date, default=date.today)
    item_category = Column(String(100), nullable=False)
    waste_kg = Column(Float, nullable=False)
    waste_cost_inr = Column(Float, nullable=False)
    primary_cause = Column(String(255), nullable=False)  # Overproduction, Spoilage, Plate Waste, Machine Loss
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float, default=0.0)
    ai_recommendation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SustainabilityReport(Base):
    __tablename__ = "sustainability_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_period = Column(String(50), nullable=False)  # e.g., "2026-Q1", "2026-10", "Annual 2026"
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Measured and calculated ESG metrics
    total_food_waste_prevented_kg = Column(Float, nullable=False)
    total_food_redistributed_kg = Column(Float, nullable=False)
    meals_supported_count = Column(Integer, nullable=False)
    
    # Documented conversion factors:
    # 1 kg food waste avoided ≈ 2.5 kg CO2e (FAO & EPA conversion methodology)
    # 1 kg food ≈ 290 liters virtual water saved
    # 1 kg food ≈ 3.2 kWh embedded energy saved
    carbon_emissions_avoided_kg_co2e = Column(Float, nullable=False)
    water_saved_liters = Column(Float, nullable=False)
    energy_saved_kwh = Column(Float, nullable=False)
    
    institutional_waste_reduction_pct = Column(Float, default=24.5)
    active_ngos_count = Column(Integer, default=12)
    active_institutions_count = Column(Integer, default=8)
    summary_notes = Column(Text, nullable=True)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="INFO")  # ALERT, INFO, DONATION, SUCCESS, WARNING
    is_read = Column(Boolean, default=False)
    related_link = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
