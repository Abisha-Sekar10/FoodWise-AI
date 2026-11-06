from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime

class WasteAnalyticsResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    date: date
    item_category: str
    waste_kg: float
    waste_cost_inr: float
    primary_cause: str
    is_anomaly: bool
    anomaly_score: float
    ai_recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True

class SustainabilityReportResponse(BaseModel):
    id: int
    report_period: str
    generated_at: datetime
    total_food_waste_prevented_kg: float
    total_food_redistributed_kg: float
    meals_supported_count: int
    carbon_emissions_avoided_kg_co2e: float
    water_saved_liters: float
    energy_saved_kwh: float
    institutional_waste_reduction_pct: float
    active_ngos_count: int
    active_institutions_count: int
    summary_notes: Optional[str] = None

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    related_link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ProductionPlanningRecommendation(BaseModel):
    item_name: str
    category: str
    recommended_production_kg: float
    recommended_portions: int
    procurement_recommendation_kg: float
    estimated_demand: int
    current_inventory_kg: float
    expiring_soon_kg: float
    historical_waste_rate_pct: float
    confidence_score: float
    reasoning: List[str]
