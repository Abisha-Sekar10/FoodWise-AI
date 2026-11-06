from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.donation import DonationStatus

class FoodDonationBase(BaseModel):
    title: str
    food_category: str
    quantity_kg: float
    portions: int
    preparation_time: datetime
    safe_use_deadline: datetime
    storage_condition: str = "Heated Container / Hot Holding (>60°C)"
    packaging_type: str = "Food-grade Insulated Cans"
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    special_instructions: Optional[str] = None
    safety_verified: bool = True

class FoodDonationCreate(FoodDonationBase):
    kitchen_id: Optional[int] = None
    surplus_id: Optional[int] = None

class PickupScheduleCreate(BaseModel):
    donation_id: int
    vehicle_type: str = "Refrigerated Van"
    driver_name: str = "Volunteer Team Alpha"
    driver_phone: str = "+91 98765 43210"
    scheduled_pickup_time: datetime
    estimated_delivery_time: datetime

class DeliveryStatusUpdate(BaseModel):
    status: DonationStatus
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    temperature_logged_celsius: Optional[float] = None
    eta_minutes: Optional[int] = None
    distance_remaining_km: Optional[float] = None
    receiver_signature_name: Optional[str] = None

class DonationResponse(FoodDonationBase):
    id: int
    donation_code: str
    kitchen_id: int
    surplus_id: Optional[int] = None
    status: DonationStatus
    accepted_ngo_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    pickup_schedule: Optional[Dict[str, Any]] = None
    tracking: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
