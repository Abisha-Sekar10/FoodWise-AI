from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class QualityAssessmentResponse(BaseModel):
    id: int
    item_name: str
    image_path: str
    visual_quality_category: str
    confidence_score: float
    detected_features: Optional[Dict[str, Any]] = None
    requires_human_inspection: bool
    human_verifier_notes: Optional[str] = None
    is_redistribution_approved: bool
    safety_disclaimer: str
    assessed_at: datetime

    class Config:
        from_attributes = True

class SensorReadingBase(BaseModel):
    sensor_id: str
    sensor_type: str
    storage_area: str
    metric_value: float
    unit: str
    threshold_min: Optional[float] = None
    threshold_max: Optional[float] = None

class SensorReadingCreate(SensorReadingBase):
    kitchen_id: int

class SensorReadingResponse(SensorReadingBase):
    id: int
    kitchen_id: int
    is_anomaly: bool
    alert_triggered: bool
    timestamp: datetime

    class Config:
        from_attributes = True
