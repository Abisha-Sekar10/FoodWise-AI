from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class FoodQualityAssessment(Base):
    __tablename__ = "food_quality_assessments"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=True)
    item_name = Column(String(255), nullable=False)
    image_path = Column(String(500), nullable=False)
    visual_quality_category = Column(String(100), nullable=False)  # Fresh / Prime, Good / Safe to Consume, Slight Deterioration, Spoiled / Unsafe
    confidence_score = Column(Float, nullable=False)  # 0.0 - 1.0
    detected_features = Column(JSON, nullable=True)  # discoloration, mold_probability, browning_index, texture_uniformity
    requires_human_inspection = Column(Boolean, default=False)
    human_verifier_notes = Column(Text, nullable=True)
    is_redistribution_approved = Column(Boolean, default=True)
    safety_disclaimer = Column(
        String(500),
        default="AI visual screening is for quality triage and does not replace certified laboratory or sensory food safety testing."
    )
    assessed_at = Column(DateTime, default=datetime.utcnow)

class IoTSensorReading(Base):
    __tablename__ = "iot_sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    sensor_id = Column(String(100), nullable=False, index=True)  # e.g., SENSOR-COLD-01
    sensor_type = Column(String(50), nullable=False)  # Temperature, Humidity, Gas/Ethylene, DoorStatus
    storage_area = Column(String(100), nullable=False)  # Walk-in Chiller 1, Deep Freezer, Dry Pantry
    metric_value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # °C, %, ppm
    threshold_min = Column(Float, nullable=True)
    threshold_max = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    alert_triggered = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    kitchen = relationship("Kitchen", back_populates="iot_sensors")
