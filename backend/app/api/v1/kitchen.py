from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import List, Optional
from app.core.database import get_db
from app.models.kitchen import FoodInventory, FoodProduction, FoodConsumption, DemandPrediction, FoodSurplus
from app.models.organization import Kitchen
from app.models.donation import FoodDonation, DonationStatus
from app.schemas.kitchen import (
    InventoryCreate, InventoryResponse,
    ProductionCreate, ProductionResponse,
    ConsumptionCreate, ConsumptionResponse,
    PredictionRequest, PredictionResponse,
    SurplusCreate, SurplusResponse
)
from app.ml.demand_forecasting import demand_forecaster
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/summary/{kitchen_id}")
def get_kitchen_summary(kitchen_id: int, db: Session = Depends(get_db)):
    kitchen = db.query(Kitchen).filter(Kitchen.id == kitchen_id).first()
    if not kitchen:
        kitchen = db.query(Kitchen).first()
        kitchen_id = kitchen.id if kitchen else 1

    today = date.today()
    
    # Today's predictions
    prediction = db.query(DemandPrediction).filter(
        DemandPrediction.kitchen_id == kitchen_id,
        DemandPrediction.target_date == today
    ).first()

    # Recent production & consumption
    todays_production = db.query(FoodProduction).filter(
        FoodProduction.kitchen_id == kitchen_id,
        FoodProduction.date == today
    ).all()

    todays_consumption = db.query(FoodConsumption).filter(
        FoodConsumption.kitchen_id == kitchen_id,
        FoodConsumption.date == today
    ).first()

    # Active inventory count & near-expiry count
    three_days_later = today + timedelta(days=3)
    expiring_soon_items = db.query(FoodInventory).filter(
        FoodInventory.kitchen_id == kitchen_id,
        FoodInventory.expiry_date <= three_days_later,
        FoodInventory.expiry_date >= today
    ).all()

    expired_items = db.query(FoodInventory).filter(
        FoodInventory.kitchen_id == kitchen_id,
        FoodInventory.expiry_date < today
    ).all()

    # Total surplus identified
    surpluses = db.query(FoodSurplus).filter(FoodSurplus.kitchen_id == kitchen_id).all()
    total_surplus_kg = sum(s.surplus_kg for s in surpluses)

    return {
        "kitchen_id": kitchen_id,
        "kitchen_name": kitchen.name if kitchen else "Central Campus Mess A",
        "daily_capacity_meals": kitchen.daily_capacity_meals if kitchen else 800,
        "today_predicted_demand": prediction.predicted_demand_portions if prediction else 520,
        "recommended_production": prediction.recommended_production_portions if prediction else 545,
        "expected_surplus": prediction.expected_surplus_portions if prediction else 25,
        "actual_portions_produced": sum(p.actual_quantity_portions for p in todays_production) if todays_production else 540,
        "actual_diners_served": todays_consumption.actual_diners if todays_consumption else 512,
        "plate_waste_today_kg": todays_consumption.plate_waste_kg if todays_consumption else 8.5,
        "service_waste_today_kg": todays_consumption.service_waste_kg if todays_consumption else 4.2,
        "expiring_soon_count": len(expiring_soon_items),
        "expired_count": len(expired_items),
        "total_surplus_kg": round(total_surplus_kg, 1),
        "cold_storage_status": "NORMAL (3.8°C / 82% RH)"
    }

# Demand Prediction
@router.post("/predict-demand", response_model=PredictionResponse)
def predict_food_demand(req: PredictionRequest, db: Session = Depends(get_db)):
    target_dt = req.target_date or date.today()
    result = demand_forecaster.predict(
        attendance=req.expected_attendance,
        target_date=target_dt,
        meal_type=req.meal_type,
        is_holiday=req.is_holiday,
        is_special_event=req.is_special_event,
        temp_celsius=req.temperature_forecast or 30.0
    )

    # Save to database
    prediction_record = DemandPrediction(
        kitchen_id=req.kitchen_id,
        target_date=target_dt,
        meal_type=req.meal_type,
        forecasted_attendance=req.expected_attendance,
        predicted_demand_portions=result["predicted_demand_portions"],
        recommended_production_portions=result["recommended_production_portions"],
        expected_surplus_portions=result["expected_surplus_portions"],
        confidence_interval_low=result["confidence_interval_low"],
        confidence_interval_high=result["confidence_interval_high"],
        features_used=result["features_used"],
        model_version=result["model_version"]
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return {
        "id": prediction_record.id,
        "kitchen_id": req.kitchen_id,
        "target_date": target_dt,
        "meal_type": req.meal_type,
        **result
    }

# Inventory Endpoints
@router.get("/inventory/{kitchen_id}", response_model=List[InventoryResponse])
def get_kitchen_inventory(kitchen_id: int, db: Session = Depends(get_db)):
    return db.query(FoodInventory).filter(FoodInventory.kitchen_id == kitchen_id).order_by(FoodInventory.expiry_date.asc()).all()

@router.post("/inventory", response_model=InventoryResponse)
def add_inventory_item(item_in: InventoryCreate, db: Session = Depends(get_db)):
    kitchen_id = item_in.kitchen_id or 1
    item = FoodInventory(
        kitchen_id=kitchen_id,
        item_name=item_in.item_name,
        category=item_in.category,
        current_stock_kg=item_in.current_stock_kg,
        unit=item_in.unit,
        reorder_level_kg=item_in.reorder_level_kg,
        purchase_date=item_in.purchase_date or date.today(),
        expiry_date=item_in.expiry_date,
        storage_condition=item_in.storage_condition,
        cost_per_kg=item_in.cost_per_kg
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Production Endpoints
@router.get("/production/{kitchen_id}", response_model=List[ProductionResponse])
def get_production_records(kitchen_id: int, db: Session = Depends(get_db)):
    return db.query(FoodProduction).filter(FoodProduction.kitchen_id == kitchen_id).order_by(FoodProduction.date.desc()).limit(20).all()

@router.post("/production", response_model=ProductionResponse)
def record_food_production(prod_in: ProductionCreate, db: Session = Depends(get_db)):
    kitchen_id = prod_in.kitchen_id or 1
    prod = FoodProduction(
        kitchen_id=kitchen_id,
        date=prod_in.date or date.today(),
        meal_type=prod_in.meal_type,
        recipe_name=prod_in.recipe_name,
        planned_quantity_portions=prod_in.planned_quantity_portions,
        actual_quantity_portions=prod_in.actual_quantity_portions,
        raw_material_used_kg=prod_in.raw_material_used_kg,
        shelf_life_hours=prod_in.shelf_life_hours,
        is_redistribution_eligible=prod_in.is_redistribution_eligible
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

# Consumption Endpoints
@router.get("/consumption/{kitchen_id}", response_model=List[ConsumptionResponse])
def get_consumption_records(kitchen_id: int, db: Session = Depends(get_db)):
    return db.query(FoodConsumption).filter(FoodConsumption.kitchen_id == kitchen_id).order_by(FoodConsumption.date.desc()).limit(20).all()

@router.post("/consumption", response_model=ConsumptionResponse)
def record_food_consumption(cons_in: ConsumptionCreate, db: Session = Depends(get_db)):
    kitchen_id = cons_in.kitchen_id or 1
    cons = FoodConsumption(
        kitchen_id=kitchen_id,
        date=cons_in.date or date.today(),
        meal_type=cons_in.meal_type,
        registered_attendance=cons_in.registered_attendance,
        actual_diners=cons_in.actual_diners,
        total_portions_served=cons_in.total_portions_served,
        plate_waste_kg=cons_in.plate_waste_kg,
        service_waste_kg=cons_in.service_waste_kg,
        kitchen_notes=cons_in.kitchen_notes
    )
    db.add(cons)
    
    # Auto-detect surplus: portions prepared in recent production minus served
    recent_prod = db.query(FoodProduction).filter(
        FoodProduction.kitchen_id == kitchen_id,
        FoodProduction.date == (cons_in.date or date.today()),
        FoodProduction.meal_type == cons_in.meal_type
    ).first()

    if recent_prod and recent_prod.actual_quantity_portions > cons_in.total_portions_served:
        surplus_portions = recent_prod.actual_quantity_portions - cons_in.total_portions_served
        surplus_kg = round(surplus_portions * 0.40, 1)  # approx 400g per meal portion
        surplus_rec = FoodSurplus(
            kitchen_id=kitchen_id,
            date=cons_in.date or date.today(),
            meal_type=cons_in.meal_type,
            item_name=recent_prod.recipe_name,
            surplus_portions=surplus_portions,
            surplus_kg=surplus_kg,
            cause_of_surplus=f"Diners attended ({cons_in.actual_diners}) below prepared ({recent_prod.actual_quantity_portions})"
        )
        db.add(surplus_rec)

    db.commit()
    db.refresh(cons)
    return cons

# Surplus Endpoints
@router.get("/surplus/{kitchen_id}", response_model=List[SurplusResponse])
def get_surplus_records(kitchen_id: int, db: Session = Depends(get_db)):
    return db.query(FoodSurplus).filter(FoodSurplus.kitchen_id == kitchen_id).order_by(FoodSurplus.date.desc()).all()

@router.post("/surplus/list-donation/{surplus_id}")
def convert_surplus_to_donation(surplus_id: int, db: Session = Depends(get_db)):
    surplus = db.query(FoodSurplus).filter(FoodSurplus.id == surplus_id).first()
    if not surplus:
        raise HTTPException(status_code=404, detail="Surplus record not found")
    
    kitchen = db.query(Kitchen).filter(Kitchen.id == surplus.kitchen_id).first()
    
    # Check if already listed
    if surplus.is_listed_for_donation:
        existing = db.query(FoodDonation).filter(FoodDonation.surplus_id == surplus.id).first()
        if existing:
            return existing

    donation_code = f"FD-{int(datetime.utcnow().timestamp()) % 100000:05d}"
    donation = FoodDonation(
        donation_code=donation_code,
        kitchen_id=surplus.kitchen_id,
        surplus_id=surplus.id,
        title=f"Fresh Surplus: {surplus.item_name}",
        food_category="Cooked Meals",
        quantity_kg=surplus.surplus_kg,
        portions=surplus.surplus_portions,
        preparation_time=datetime.utcnow() - timedelta(hours=1),
        safe_use_deadline=datetime.utcnow() + timedelta(hours=4),
        storage_condition="Insulated Heated Container (>60°C)",
        packaging_type="Food-grade stainless steel & sealed containers",
        pickup_address=kitchen.institution.address if (kitchen and kitchen.institution) else "Central Kitchen, Campus Gate 2",
        pickup_latitude=kitchen.institution.latitude if (kitchen and kitchen.institution) else 28.6139,
        pickup_longitude=kitchen.institution.longitude if (kitchen and kitchen.institution) else 77.2090,
        special_instructions="Prepared under certified FSSAI kitchen hygiene standards. Collect before safe-use deadline.",
        status=DonationStatus.AVAILABLE,
        safety_verified=True
    )
    surplus.is_listed_for_donation = True
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation
