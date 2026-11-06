from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Optional
from app.core.database import get_db
from app.models.organization import FoodProcessingUnit
from app.models.processing import ProductionRecord, MachineMonitoring, EnergyConsumption
from app.schemas.processing import (
    ProductionRecordCreate, ProductionRecordResponse,
    MachineMonitoringCreate, MachineMonitoringResponse,
    EnergyConsumptionCreate, EnergyConsumptionResponse
)
from app.ml.anomaly_detector import anomaly_detector

router = APIRouter()

@router.get("/summary/{unit_id}")
def get_processing_unit_summary(unit_id: int = 1, db: Session = Depends(get_db)):
    unit = db.query(FoodProcessingUnit).filter(FoodProcessingUnit.id == unit_id).first()
    if not unit:
        unit = db.query(FoodProcessingUnit).first()
        unit_id = unit.id if unit else 1

    records = db.query(ProductionRecord).filter(ProductionRecord.unit_id == unit_id).all()
    machines = db.query(MachineMonitoring).filter(MachineMonitoring.unit_id == unit_id).all()
    energy_logs = db.query(EnergyConsumption).filter(EnergyConsumption.unit_id == unit_id).all()

    total_input = sum(r.raw_material_input_kg for r in records)
    total_output = sum(r.finished_product_output_kg for r in records)
    total_loss = sum(r.material_loss_kg for r in records)
    avg_efficiency = round((total_output / total_input * 100) if total_input > 0 else 89.4, 1)

    total_downtime = sum(m.downtime_minutes for m in machines)
    total_energy_kwh = sum(e.electricity_kwh for e in energy_logs)
    total_water_liters = sum(e.water_liters for e in energy_logs)

    # Anomaly checks
    records_dict = [
        {"batch_number": r.batch_number, "production_efficiency_pct": r.production_efficiency_pct, "material_loss_kg": r.material_loss_kg}
        for r in records
    ]
    machines_dict = [
        {"machine_code": m.machine_code, "downtime_minutes": m.downtime_minutes, "temperature_celsius": m.temperature_celsius, "vibration_mm_s": m.vibration_mm_s}
        for m in machines
    ]
    energy_dict = [
        {"shift": e.shift, "specific_energy_kwh_per_kg": e.specific_energy_kwh_per_kg, "is_abnormal_consumption": e.is_abnormal_consumption}
        for e in energy_logs
    ]

    anomalies = anomaly_detector.detect_processing_anomalies(records_dict, machines_dict, energy_dict)

    return {
        "unit_id": unit_id,
        "unit_name": unit.name if unit else "AgroFresh Agro-Industrial Unit 3",
        "sector": unit.sector if unit else "Fruit & Vegetable Processing & Canning",
        "daily_capacity_tons": unit.daily_processing_capacity_tons if unit else 15.0,
        "total_raw_material_input_kg": round(total_input, 1),
        "total_finished_product_output_kg": round(total_output, 1),
        "total_material_loss_kg": round(total_loss, 1),
        "production_efficiency_pct": avg_efficiency,
        "total_machine_downtime_minutes": round(total_downtime, 1),
        "total_electricity_kwh": round(total_energy_kwh, 1),
        "total_water_liters": round(total_water_liters, 1),
        "active_machines_count": len(machines),
        "anomalies_detected": anomalies
    }

@router.get("/production-records/{unit_id}", response_model=List[ProductionRecordResponse])
def get_production_records(unit_id: int = 1, db: Session = Depends(get_db)):
    return db.query(ProductionRecord).filter(ProductionRecord.unit_id == unit_id).order_by(ProductionRecord.date.desc()).all()

@router.post("/production-records", response_model=ProductionRecordResponse)
def add_production_record(rec_in: ProductionRecordCreate, db: Session = Depends(get_db)):
    unit_id = rec_in.unit_id or 1
    material_loss = max(0.0, rec_in.raw_material_input_kg - rec_in.finished_product_output_kg)
    efficiency = round((rec_in.finished_product_output_kg / rec_in.raw_material_input_kg) * 100, 2) if rec_in.raw_material_input_kg > 0 else 0.0
    variance = round(((rec_in.finished_product_output_kg - rec_in.planned_production_kg) / rec_in.planned_production_kg) * 100, 2) if rec_in.planned_production_kg > 0 else 0.0

    record = ProductionRecord(
        unit_id=unit_id,
        batch_number=rec_in.batch_number,
        product_name=rec_in.product_name,
        date=rec_in.date or date.today(),
        raw_material_input_kg=rec_in.raw_material_input_kg,
        finished_product_output_kg=rec_in.finished_product_output_kg,
        material_loss_kg=material_loss,
        production_efficiency_pct=efficiency,
        planned_production_kg=rec_in.planned_production_kg,
        variance_pct=variance
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/machines/{unit_id}", response_model=List[MachineMonitoringResponse])
def get_machines(unit_id: int = 1, db: Session = Depends(get_db)):
    return db.query(MachineMonitoring).filter(MachineMonitoring.unit_id == unit_id).all()

@router.post("/machines", response_model=MachineMonitoringResponse)
def add_machine_log(m_in: MachineMonitoringCreate, db: Session = Depends(get_db)):
    unit_id = m_in.unit_id or 1
    m = MachineMonitoring(
        unit_id=unit_id,
        machine_name=m_in.machine_name,
        machine_code=m_in.machine_code,
        status=m_in.status,
        operating_hours=m_in.operating_hours,
        downtime_minutes=m_in.downtime_minutes,
        downtime_reason=m_in.downtime_reason,
        temperature_celsius=m_in.temperature_celsius,
        vibration_mm_s=m_in.vibration_mm_s,
        pressure_bar=m_in.pressure_bar,
        maintenance_due_date=m_in.maintenance_due_date
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/energy/{unit_id}", response_model=List[EnergyConsumptionResponse])
def get_energy_records(unit_id: int = 1, db: Session = Depends(get_db)):
    return db.query(EnergyConsumption).filter(EnergyConsumption.unit_id == unit_id).order_by(EnergyConsumption.date.desc()).all()

@router.post("/energy", response_model=EnergyConsumptionResponse)
def add_energy_record(e_in: EnergyConsumptionCreate, db: Session = Depends(get_db)):
    unit_id = e_in.unit_id or 1
    sec = round(e_in.electricity_kwh / max(1.0, e_in.total_output_kg), 3)
    is_abnormal = sec > 0.40

    record = EnergyConsumption(
        unit_id=unit_id,
        date=e_in.date or date.today(),
        shift=e_in.shift,
        electricity_kwh=e_in.electricity_kwh,
        water_liters=e_in.water_liters,
        fuel_liters=e_in.fuel_liters,
        specific_energy_kwh_per_kg=sec,
        is_abnormal_consumption=is_abnormal,
        alert_notes=e_in.alert_notes or ("Specific energy consumption exceeds benchmark" if is_abnormal else None)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
