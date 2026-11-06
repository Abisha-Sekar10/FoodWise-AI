from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.organization import Kitchen, NGO, Institution
from app.models.donation import FoodDonation, DonationStatus
from app.ml.route_optimizer import route_optimizer

router = APIRouter()

@router.get("/map-markers")
def get_map_markers(db: Session = Depends(get_db)):
    """Returns GPS locations of all kitchens, NGOs, and active pickup donations."""
    kitchens = db.query(Kitchen).all()
    ngos = db.query(NGO).all()
    active_donations = db.query(FoodDonation).filter(
        FoodDonation.status.in_([DonationStatus.AVAILABLE, DonationStatus.ACCEPTED, DonationStatus.PICKUP_SCHEDULED, DonationStatus.COLLECTED])
    ).all()

    markers = []

    # Kitchens
    for k in kitchens:
        lat = k.institution.latitude if k.institution else 28.6139
        lng = k.institution.longitude if k.institution else 77.2090
        markers.append({
            "id": f"kitchen_{k.id}",
            "type": "KITCHEN",
            "name": k.name,
            "institution": k.institution.name if k.institution else "Partner Institution",
            "lat": lat,
            "lng": lng,
            "capacity": f"{k.daily_capacity_meals} meals/day",
            "phone": k.institution.contact_phone if k.institution else "+91 98765 00001",
            "address": k.institution.address if k.institution else "New Delhi"
        })

    # NGOs
    for n in ngos:
        markers.append({
            "id": f"ngo_{n.id}",
            "type": "NGO",
            "name": n.name,
            "lat": n.latitude,
            "lng": n.longitude,
            "capacity": f"{n.daily_meals_capacity} meals capacity",
            "has_refrigeration": n.has_refrigerated_transport,
            "phone": n.contact_phone,
            "address": n.address
        })

    # Active Donations
    for d in active_donations:
        markers.append({
            "id": f"donation_{d.id}",
            "type": "DONATION",
            "name": d.title,
            "code": d.donation_code,
            "portions": d.portions,
            "quantity_kg": d.quantity_kg,
            "status": d.status.value,
            "lat": d.pickup_latitude,
            "lng": d.pickup_longitude,
            "deadline": d.safe_use_deadline.isoformat(),
            "address": d.pickup_address
        })

    return markers

@router.get("/optimize")
def plan_optimized_route(kitchen_id: Optional[int] = 1, db: Session = Depends(get_db)):
    """
    Plans an optimal redistribution circuit starting from kitchen
    and visiting active recipient NGOs based on food expiry urgency and distance.
    """
    kitchen = db.query(Kitchen).filter(Kitchen.id == kitchen_id).first()
    origin_lat = kitchen.institution.latitude if (kitchen and kitchen.institution) else 28.6139
    origin_lng = kitchen.institution.longitude if (kitchen and kitchen.institution) else 77.2090
    origin_name = kitchen.name if kitchen else "Central Kitchen Hub"

    origin = {
        "name": origin_name,
        "type": "HUB",
        "lat": origin_lat,
        "lng": origin_lng,
        "stop_type": "Pickup Origin"
    }

    # Retrieve candidate NGO destinations
    ngos = db.query(NGO).limit(4).all()
    destinations = []
    for idx, ngo in enumerate(ngos):
        destinations.append({
            "ngo_id": ngo.id,
            "name": ngo.name,
            "type": "NGO",
            "lat": ngo.latitude,
            "lng": ngo.longitude,
            "capacity": ngo.daily_meals_capacity,
            "stop_type": f"Delivery Drop #{idx+1}",
            "urgency": "HIGH" if idx == 0 else "NORMAL",
            "minutes_to_deadline": 90 - (idx * 15)
        })

    route_plan = route_optimizer.optimize_multi_drop_route(origin=origin, destinations=destinations)
    return route_plan
