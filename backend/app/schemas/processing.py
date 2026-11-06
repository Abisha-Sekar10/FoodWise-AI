from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ProductionRecordBase(BaseModel):
    batch_number: str
    product_name: str
    date: Optional[date] = None
    raw_material_input_kg: float
    finished_product_output_kg: float
    planned_production_kg: float

class ProductionRecordCreate(ProductionRecordBase):
    unit_id: Optional[int] = None

class ProductionRecordResponse(ProductionRecordBase):
    id: int
    unit_id: int
    material_loss_kg: float
    production_efficiency_pct: float
    variance_pct: float
    created_at: datetime

    class Config:
        from_attributes = True

class MachineMonitoringBase(BaseModel):
    machine_name: str
    machine_code: str
    status: str = "OPERATIONAL"
    operating_hours: float = 8.0
    downtime_minutes: float = 0.0
    downtime_reason: Optional[str] = None
    temperature_celsius: float = 75.0
    vibration_mm_s: float = 1.2
    pressure_bar: float = 3.5
    maintenance_due_date: Optional[date] = None

class MachineMonitoringCreate(MachineMonitoringBase):
    unit_id: Optional[int] = None

class MachineMonitoringResponse(MachineMonitoringBase):
    id: int
    unit_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class EnergyConsumptionBase(BaseModel):
    shift: str = "Morning Shift"
    electricity_kwh: float
    water_liters: float
    fuel_liters: float = 0.0
    total_output_kg: float = 1000.0  # Used to compute specific energy
    alert_notes: Optional[str] = None

class EnergyConsumptionCreate(EnergyConsumptionBase):
    unit_id: Optional[int] = None
    date: Optional[date] = None

class EnergyConsumptionResponse(BaseModel):
    id: int
    unit_id: int
    date: date
    shift: str
    electricity_kwh: float
    water_liters: float
    fuel_liters: float
    specific_energy_kwh_per_kg: float
    is_abnormal_consumption: bool
    alert_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
