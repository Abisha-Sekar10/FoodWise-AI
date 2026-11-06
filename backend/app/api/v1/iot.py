from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import random
from typing import List
from app.core.database import get_db
from app.models.quality import IoTSensorReading
from app.models.analytics import Notification
from app.schemas.quality import SensorReadingCreate, SensorReadingResponse

router = APIRouter()

# Safety thresholds per storage area
STORAGE_THRESHOLDS = {
    "Walk-in Chiller (Dairy & Produce)": {"min_temp": 1.0, "max_temp": 4.5, "min_rh": 75.0, "max_rh": 90.0},
    "Deep Freezer (Meat & Frozen)": {"min_temp": -22.0, "max_temp": -18.0, "min_rh": 40.0, "max_rh": 70.0},
    "Dry Grain Pantry": {"min_temp": 18.0, "max_temp": 24.0, "min_rh": 40.0, "max_rh": 60.0},
    "Cooked Food Holding Area": {"min_temp": 60.0, "max_temp": 75.0, "min_rh": 30.0, "max_rh": 80.0}
}

@router.get("/live-readings/{kitchen_id}")
def get_live_iot_readings(kitchen_id: int, db: Session = Depends(get_db)):
    readings = db.query(IoTSensorReading).filter(
        IoTSensorReading.kitchen_id == kitchen_id
    ).order_by(IoTSensorReading.timestamp.desc()).limit(20).all()

    # If no readings yet, return default baseline telemetry with simulation notice
    if not readings:
        return {
            "mode": "Simulated IoT Telemetry",
            "is_simulated": True,
            "sensors": [
                {
                    "sensor_id": "IOT-CHILLER-01",
                    "storage_area": "Walk-in Chiller (Dairy & Produce)",
                    "temperature_celsius": 3.6,
                    "humidity_percent": 82.5,
                    "ethylene_ppm": 0.08,
                    "door_status": "CLOSED",
                    "status": "NORMAL",
                    "safe_temp_range": "1.0°C - 4.5°C",
                    "last_updated": datetime.utcnow().strftime("%H:%M:%S")
                },
                {
                    "sensor_id": "IOT-FREEZER-02",
                    "storage_area": "Deep Freezer (Meat & Frozen)",
                    "temperature_celsius": -19.4,
                    "humidity_percent": 55.0,
                    "ethylene_ppm": 0.01,
                    "door_status": "CLOSED",
                    "status": "NORMAL",
                    "safe_temp_range": "-22.0°C - -18.0°C",
                    "last_updated": datetime.utcnow().strftime("%H:%M:%S")
                },
                {
                    "sensor_id": "IOT-PANTRY-03",
                    "storage_area": "Dry Grain Pantry",
                    "temperature_celsius": 21.8,
                    "humidity_percent": 52.0,
                    "ethylene_ppm": 0.03,
                    "door_status": "CLOSED",
                    "status": "NORMAL",
                    "safe_temp_range": "18.0°C - 24.0°C",
                    "last_updated": datetime.utcnow().strftime("%H:%M:%S")
                },
                {
                    "sensor_id": "IOT-HOT-HOLD-04",
                    "storage_area": "Cooked Food Holding Area",
                    "temperature_celsius": 64.2,
                    "humidity_percent": 45.0,
                    "ethylene_ppm": 0.02,
                    "door_status": "CLOSED",
                    "status": "NORMAL",
                    "safe_temp_range": "> 60.0°C (FSSAI Hot Holding)",
                    "last_updated": datetime.utcnow().strftime("%H:%M:%S")
                }
            ]
        }

    return {
        "mode": "Simulated IoT Telemetry",
        "is_simulated": True,
        "readings": readings
    }

@router.post("/simulate-telemetry/{kitchen_id}")
def simulate_sensor_telemetry(kitchen_id: int, trigger_anomaly: bool = False, db: Session = Depends(get_db)):
    """Simulates realistic IoT sensor broadcast. If trigger_anomaly=True, introduces temperature spike."""
    areas = [
        ("IOT-CHILLER-01", "Walk-in Chiller (Dairy & Produce)", "Temperature", 3.4 if not trigger_anomaly else 8.9, "°C", 1.0, 4.5),
        ("IOT-FREEZER-02", "Deep Freezer (Meat & Frozen)", "Temperature", -19.2, "°C", -22.0, -18.0),
        ("IOT-PANTRY-03", "Dry Grain Pantry", "Humidity", 52.0, "%", 40.0, 60.0)
    ]

    created = []
    for s_id, area, s_type, val, unit, t_min, t_max in areas:
        is_anom = val < t_min or val > t_max
        r = IoTSensorReading(
            kitchen_id=kitchen_id,
            sensor_id=s_id,
            sensor_type=s_type,
            storage_area=area,
            metric_value=round(val + random.uniform(-0.2, 0.2), 2),
            unit=unit,
            threshold_min=t_min,
            threshold_max=t_max,
            is_anomaly=is_anom,
            alert_triggered=is_anom
        )
        db.add(r)
        created.append(r)

    db.commit()
    return {"message": "Telemetry broadcast processed", "trigger_anomaly": trigger_anomaly, "sensors_count": len(created)}
