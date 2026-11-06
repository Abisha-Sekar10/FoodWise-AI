from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# Inventory Schemas
class InventoryBase(BaseModel):
    item_name: str
    category: str
    current_stock_kg: float
    unit: str = "kg"
    reorder_level_kg: float = 10.0
    purchase_date: Optional[date] = None
    expiry_date: date
    storage_condition: str = "Ambient"
    cost_per_kg: float = 50.0

class InventoryCreate(InventoryBase):
    kitchen_id: Optional[int] = None

class InventoryResponse(InventoryBase):
    id: int
    kitchen_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Production Schemas
class ProductionBase(BaseModel):
    meal_type: str
    recipe_name: str
    planned_quantity_portions: int
    actual_quantity_portions: int
    raw_material_used_kg: float = 0.0
    shelf_life_hours: float = 6.0
    is_redistribution_eligible: bool = True

class ProductionCreate(ProductionBase):
    kitchen_id: Optional[int] = None
    date: Optional[date] = None

class ProductionResponse(ProductionBase):
    id: int
    kitchen_id: int
    date: date
    preparation_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# Consumption Schemas
class ConsumptionBase(BaseModel):
    meal_type: str
    registered_attendance: int
    actual_diners: int
    total_portions_served: int
    plate_waste_kg: float = 0.0
    service_waste_kg: float = 0.0
    kitchen_notes: Optional[str] = None

class ConsumptionCreate(ConsumptionBase):
    kitchen_id: Optional[int] = None
    date: Optional[date] = None

class ConsumptionResponse(ConsumptionBase):
    id: int
    kitchen_id: int
    date: date
    created_at: datetime

    class Config:
        from_attributes = True

# Demand Prediction Schemas
class PredictionRequest(BaseModel):
    kitchen_id: int
    target_date: Optional[date] = None
    meal_type: str = "Lunch"
    expected_attendance: int
    day_of_week: Optional[str] = None
    is_holiday: bool = False
    is_special_event: bool = False
    temperature_forecast: Optional[float] = 30.0

class PredictionResponse(BaseModel):
    id: Optional[int] = None
    kitchen_id: int
    target_date: date
    meal_type: str
    forecasted_attendance: int
    predicted_demand_portions: int
    recommended_production_portions: int
    expected_surplus_portions: int
    confidence_interval_low: int
    confidence_interval_high: int
    features_used: Optional[Dict[str, Any]] = None
    model_version: str
    explanation: str

# Surplus Schemas
class SurplusBase(BaseModel):
    meal_type: str
    item_name: str
    surplus_portions: int
    surplus_kg: float
    cause_of_surplus: str = "Overestimation of attendance"

class SurplusCreate(SurplusBase):
    kitchen_id: Optional[int] = None
    date: Optional[date] = None

class SurplusResponse(SurplusBase):
    id: int
    kitchen_id: int
    date: date
    is_listed_for_donation: bool
    created_at: datetime

    class Config:
        from_attributes = True
