from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from app.core.database import get_db
from app.models.donation import FoodDonation, DonationRequest, PickupSchedule, DeliveryTracking, DonationStatus
from app.models.organization import NGO, Kitchen
from app.models.user import User
from app.models.analytics import Notification
from app.schemas.donation import (
    FoodDonationCreate, DonationResponse,
    PickupScheduleCreate, DeliveryStatusUpdate
)
from app.ml.route_optimizer import route_optimizer
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/donations", response_model=List[DonationResponse])
def get_donations(
    status: Optional[str] = None,
    category: Optional[str] = None,
    ngo_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(FoodDonation)
    if status:
        query = query.filter(FoodDonation.status == status)
    if category:
        query = query.filter(FoodDonation.food_category == category)
    if ngo_id:
        query = query.filter(FoodDonation.accepted_ngo_id == ngo_id)

    donations = query.order_by(FoodDonation.safe_use_deadline.asc()).all()

    # Enrich with pickup and tracking info
    results = []
    for d in donations:
        pickup_info = None
        if d.pickup_schedule:
            pickup_info = {
                "vehicle_type": d.pickup_schedule.vehicle_type,
                "driver_name": d.pickup_schedule.driver_name,
                "driver_phone": d.pickup_schedule.driver_phone,
                "scheduled_pickup_time": d.pickup_schedule.scheduled_pickup_time.isoformat() if d.pickup_schedule.scheduled_pickup_time else None
            }
        tracking_info = None
        if d.tracking:
            tracking_info = {
                "current_status": d.tracking.current_status.value if d.tracking.current_status else None,
                "eta_minutes": d.tracking.eta_minutes,
                "distance_remaining_km": d.tracking.distance_remaining_km,
                "temperature_logged_celsius": d.tracking.temperature_logged_celsius,
                "delivered_at": d.tracking.delivered_at.isoformat() if d.tracking.delivered_at else None
            }

        results.append({
            "id": d.id,
            "donation_code": d.donation_code,
            "kitchen_id": d.kitchen_id,
            "surplus_id": d.surplus_id,
            "title": d.title,
            "food_category": d.food_category,
            "quantity_kg": d.quantity_kg,
            "portions": d.portions,
            "preparation_time": d.preparation_time,
            "safe_use_deadline": d.safe_use_deadline,
            "storage_condition": d.storage_condition,
            "packaging_type": d.packaging_type,
            "pickup_address": d.pickup_address,
            "pickup_latitude": d.pickup_latitude,
            "pickup_longitude": d.pickup_longitude,
            "special_instructions": d.special_instructions,
            "status": d.status,
            "safety_verified": d.safety_verified,
            "accepted_ngo_id": d.accepted_ngo_id,
            "created_at": d.created_at,
            "updated_at": d.updated_at,
            "pickup_schedule": pickup_info,
            "tracking": tracking_info
        })
    return results

@router.get("/matching-ngos/{donation_id}")
def get_matching_ngos(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(FoodDonation).filter(FoodDonation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    ngos = db.query(NGO).filter(NGO.is_verified == True).all()
    matches = []

    for ngo in ngos:
        # Distance calculation
        distance_km = route_optimizer.haversine_distance(
            donation.pickup_latitude, donation.pickup_longitude,
            ngo.latitude, ngo.longitude
        )

        # Capacity suitability
        capacity_match = ngo.daily_meals_capacity >= donation.portions
        # Estimated transit time
        est_transit_minutes = int(round((distance_km / 28.0) * 60))
        
        # Safe pickup feasibility: check if transit + buffer fits inside deadline
        mins_remaining = int((donation.safe_use_deadline - datetime.utcnow()).total_seconds() / 60)
        is_feasible = (mins_remaining - est_transit_minutes) > 30

        # Match score (0-100)
        score = 100
        score -= min(40, distance_km * 2.5)  # distance penalty
        if not capacity_match:
            score -= 20
        if not is_feasible:
            score -= 30
        if ngo.has_refrigerated_transport:
            score += 10

        matches.append({
            "ngo_id": ngo.id,
            "ngo_name": ngo.name,
            "distance_km": round(distance_km, 1),
            "estimated_travel_minutes": est_transit_minutes,
            "capacity_meals": ngo.daily_meals_capacity,
            "has_refrigerated_van": ngo.has_refrigerated_transport,
            "match_score": max(20, min(99, int(score))),
            "is_feasible": is_feasible,
            "phone": ngo.contact_phone,
            "address": ngo.address
        })

    # Sort by match score descending
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches

@router.post("/accept/{donation_id}")
def accept_donation(
    donation_id: int,
    ngo_id: int = Query(...),
    db: Session = Depends(get_db)
):
    donation = db.query(FoodDonation).filter(FoodDonation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    if donation.status != DonationStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail=f"Donation is already {donation.status.value}")

    donation.status = DonationStatus.ACCEPTED
    donation.accepted_ngo_id = ngo_id

    # Create Tracking Record
    tracking = DeliveryTracking(
        donation_id=donation.id,
        current_status=DonationStatus.ACCEPTED,
        current_latitude=donation.pickup_latitude,
        current_longitude=donation.pickup_longitude,
        eta_minutes=35,
        distance_remaining_km=6.4,
        temperature_logged_celsius=5.2
    )
    db.add(tracking)
    db.commit()
    return {"message": "Donation accepted successfully", "donation_code": donation.donation_code, "status": donation.status.value}

@router.post("/schedule-pickup")
def schedule_pickup(schedule_in: PickupScheduleCreate, db: Session = Depends(get_db)):
    donation = db.query(FoodDonation).filter(FoodDonation.id == schedule_in.donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    existing = db.query(PickupSchedule).filter(PickupSchedule.donation_id == schedule_in.donation_id).first()
    if existing:
        existing.vehicle_type = schedule_in.vehicle_type
        existing.driver_name = schedule_in.driver_name
        existing.driver_phone = schedule_in.driver_phone
        existing.scheduled_pickup_time = schedule_in.scheduled_pickup_time
        existing.estimated_delivery_time = schedule_in.estimated_delivery_time
    else:
        pickup = PickupSchedule(
            donation_id=schedule_in.donation_id,
            vehicle_type=schedule_in.vehicle_type,
            driver_name=schedule_in.driver_name,
            driver_phone=schedule_in.driver_phone,
            scheduled_pickup_time=schedule_in.scheduled_pickup_time,
            estimated_delivery_time=schedule_in.estimated_delivery_time
        )
        db.add(pickup)

    donation.status = DonationStatus.PICKUP_SCHEDULED
    if donation.tracking:
        donation.tracking.current_status = DonationStatus.PICKUP_SCHEDULED

    db.commit()
    return {"message": "Pickup scheduled successfully", "status": donation.status.value}

@router.post("/update-status/{donation_id}")
def update_delivery_status(donation_id: int, status_update: DeliveryStatusUpdate, db: Session = Depends(get_db)):
    donation = db.query(FoodDonation).filter(FoodDonation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    donation.status = status_update.status
    if donation.tracking:
        donation.tracking.current_status = status_update.status
        if status_update.current_latitude:
            donation.tracking.current_latitude = status_update.current_latitude
        if status_update.current_longitude:
            donation.tracking.current_longitude = status_update.current_longitude
        if status_update.eta_minutes is not None:
            donation.tracking.eta_minutes = status_update.eta_minutes
        if status_update.distance_remaining_km is not None:
            donation.tracking.distance_remaining_km = status_update.distance_remaining_km
        if status_update.temperature_logged_celsius is not None:
            donation.tracking.temperature_logged_celsius = status_update.temperature_logged_celsius
        if status_update.status in [DonationStatus.DELIVERED, DonationStatus.COMPLETED]:
            donation.tracking.delivered_at = datetime.utcnow()
            donation.tracking.receiver_signature_name = status_update.receiver_signature_name or "Verified Food Bank Incharge"

    db.commit()
    return {"message": f"Status updated to {status_update.status.value}", "status": donation.status.value}
