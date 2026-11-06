from datetime import date, datetime, timedelta
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Institution, Kitchen, FoodProcessingUnit, NGO
from app.models.kitchen import FoodInventory, FoodProduction, FoodConsumption, DemandPrediction, FoodSurplus
from app.models.donation import FoodDonation, PickupSchedule, DeliveryTracking, DonationStatus
from app.models.processing import ProductionRecord, MachineMonitoring, EnergyConsumption
from app.models.quality import FoodQualityAssessment, IoTSensorReading
from app.models.analytics import SustainabilityReport, WasteAnalytics, Notification

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if already seeded
    if db.query(User).filter(User.email == "admin@foodwise.gov.in").first():
        print("Database already contains seed users. Skipping duplicate seeding.")
        db.close()
        return

    print("Seeding FoodWise AI Database with realistic initial data...")

    # 1. Institutions
    i1 = Institution(
        name="Delhi Technical University (Hostel Mess Complex)",
        type="College Cafeteria & Dining Complex",
        address="Shahbad Daulatpur, Main Bawana Road, Delhi 110042",
        city="New Delhi",
        state="Delhi",
        latitude=28.7495,
        longitude=77.1180,
        contact_email="canteen@dtu.ac.in",
        contact_phone="+91 11 27871018",
        fssai_license="FSSAI-10022011000842",
        is_verified=True
    )
    i2 = Institution(
        name="Grand Imperial Hotel & Convention Center",
        type="Luxury Hotel & Catering Service",
        address="Connaught Place, Central Delhi 110001",
        city="New Delhi",
        state="Delhi",
        latitude=28.6315,
        longitude=77.2167,
        contact_email="banquets@grandimperial.com",
        contact_phone="+91 11 43567890",
        fssai_license="FSSAI-10018011000311",
        is_verified=True
    )
    db.add_all([i1, i2])
    db.commit()

    # 2. Kitchens
    k1 = Kitchen(
        institution_id=i1.id,
        name="Central Campus Mess Hall A",
        daily_capacity_meals=850,
        service_type="Student Buffet & Meal Trays",
        storage_capacity_kg=1200.0,
        has_cold_storage=True
    )
    k2 = Kitchen(
        institution_id=i2.id,
        name="Royal Banquet Production Kitchen",
        daily_capacity_meals=1200,
        service_type="Event Buffet & Continental Banquets",
        storage_capacity_kg=2500.0,
        has_cold_storage=True
    )
    db.add_all([k1, k2])
    db.commit()

    # 3. Food Processing Units
    p1 = FoodProcessingUnit(
        name="AgroFresh Foods Processing Unit 3",
        sector="Fruit & Vegetable Processing & Canning",
        location="Sector 63 Industrial Area, Noida",
        daily_processing_capacity_tons=15.0,
        latitude=28.6186,
        longitude=77.3789,
        contact_email="plant3@agrofresh.in",
        contact_phone="+91 120 4589201"
    )
    p2 = FoodProcessingUnit(
        name="DairyPure Integrated Processing Plant",
        sector="Dairy, Paneer & Whey Processing",
        location="Okhla Industrial Area Phase 1, New Delhi",
        daily_processing_capacity_tons=25.0,
        latitude=28.5284,
        longitude=77.2798,
        contact_email="operations@dairypure.in",
        contact_phone="+91 11 26810943"
    )
    db.add_all([p1, p2])
    db.commit()

    # 4. NGOs & Food Banks
    ngo1 = NGO(
        name="Aahaar Food Bank Foundation",
        registration_number="DARPAN-DL-2021-00918",
        address="Paharganj Community Center, New Delhi 110055",
        city="New Delhi",
        latitude=28.6433,
        longitude=77.2144,
        contact_email="contact@aahaarngo.org",
        contact_phone="+91 98112 34567",
        daily_meals_capacity=450,
        preferred_food_categories="Cooked Meals, Breads, Fruits, Packaged Foods",
        has_refrigerated_transport=True,
        is_verified=True
    )
    ngo2 = NGO(
        name="Robin Hood Army Delhi Central Chapter",
        registration_number="DARPAN-DL-2018-04192",
        address="Lajpat Nagar Volunteer Depot, New Delhi 110024",
        city="New Delhi",
        latitude=28.5684,
        longitude=77.2435,
        contact_email="delhi@robinhoodarmy.com",
        contact_phone="+91 98991 87654",
        daily_meals_capacity=600,
        preferred_food_categories="Cooked Rice, Dal, Roti, Fresh Produce",
        has_refrigerated_transport=True,
        is_verified=True
    )
    ngo3 = NGO(
        name="Roti Bank Social Welfare Trust",
        registration_number="DARPAN-DL-2020-08124",
        address="Sarai Kale Khan Relief Base, New Delhi 110013",
        city="New Delhi",
        latitude=28.5912,
        longitude=77.2560,
        contact_email="help@rotibankdelhi.org",
        contact_phone="+91 97115 67890",
        daily_meals_capacity=350,
        preferred_food_categories="Cooked Meals, Breads, Dry Rations",
        has_refrigerated_transport=False,
        is_verified=True
    )
    db.add_all([ngo1, ngo2, ngo3])
    db.commit()

    # 5. Core Users with Passwords
    hashed_pw = get_password_hash("Password123!")
    users = [
        User(
            email="admin@foodwise.gov.in",
            hashed_password=hashed_pw,
            full_name="Dr. Rajesh Sharma (MoFPI Oversight)",
            role=UserRole.ADMIN,
            phone="+91 11 23381234"
        ),
        User(
            email="kitchen@delhitechnical.edu",
            hashed_password=hashed_pw,
            full_name="Ananya Desai (Executive Mess Lead)",
            role=UserRole.KITCHEN_MANAGER,
            phone="+91 98711 22334",
            institution_id=i1.id,
            kitchen_id=k1.id
        ),
        User(
            email="processing@agrofresh.in",
            hashed_password=hashed_pw,
            full_name="Vikram Malhotra (Plant Operations Lead)",
            role=UserRole.PROCESSING_MANAGER,
            phone="+91 99882 33445",
            processing_unit_id=p1.id
        ),
        User(
            email="contact@aahaarngo.org",
            hashed_password=hashed_pw,
            full_name="Meera Sen (Aahaar NGO Director)",
            role=UserRole.NGO,
            phone="+91 98112 34567",
            ngo_id=ngo1.id
        )
    ]
    db.add_all(users)
    db.commit()

    # 6. Inventory Items (with near-expiry for testing alerts)
    today = date.today()
    inv_items = [
        FoodInventory(kitchen_id=k1.id, item_name="Basmati Rice (Grade A)", category="Grains", current_stock_kg=180.0, unit="kg", reorder_level_kg=50.0, purchase_date=today - timedelta(days=15), expiry_date=today + timedelta(days=90), storage_condition="Dry Pantry", cost_per_kg=65.0),
        FoodInventory(kitchen_id=k1.id, item_name="Toor Dal (Arhar)", category="Lentils", current_stock_kg=95.0, unit="kg", reorder_level_kg=30.0, purchase_date=today - timedelta(days=20), expiry_date=today + timedelta(days=60), storage_condition="Dry Pantry", cost_per_kg=140.0),
        FoodInventory(kitchen_id=k1.id, item_name="Fresh Full Cream Milk", category="Dairy", current_stock_kg=40.0, unit="Liters", reorder_level_kg=20.0, purchase_date=today - timedelta(days=1), expiry_date=today + timedelta(days=1), storage_condition="Cold Storage (3.5°C)", cost_per_kg=62.0),
        FoodInventory(kitchen_id=k1.id, item_name="Fresh Paneer (Cottage Cheese)", category="Dairy", current_stock_kg=18.5, unit="kg", reorder_level_kg=10.0, purchase_date=today - timedelta(days=2), expiry_date=today + timedelta(days=2), storage_condition="Cold Storage (2.0°C)", cost_per_kg=320.0),
        FoodInventory(kitchen_id=k1.id, item_name="Tomatoes (Grade 1)", category="Vegetables", current_stock_kg=35.0, unit="kg", reorder_level_kg=15.0, purchase_date=today - timedelta(days=3), expiry_date=today + timedelta(days=3), storage_condition="Ambient Chilled", cost_per_kg=40.0),
        FoodInventory(kitchen_id=k1.id, item_name="Potatoes", category="Vegetables", current_stock_kg=120.0, unit="kg", reorder_level_kg=40.0, purchase_date=today - timedelta(days=7), expiry_date=today + timedelta(days=25), storage_condition="Dry Ventilated", cost_per_kg=25.0),
        FoodInventory(kitchen_id=k1.id, item_name="Whole Wheat Atta Flour", category="Grains", current_stock_kg=150.0, unit="kg", reorder_level_kg=50.0, purchase_date=today - timedelta(days=10), expiry_date=today + timedelta(days=45), storage_condition="Dry Pantry", cost_per_kg=38.0),
        FoodInventory(kitchen_id=k1.id, item_name="Cooking Sunflower Oil", category="Oils & Fats", current_stock_kg=60.0, unit="Liters", reorder_level_kg=25.0, purchase_date=today - timedelta(days=30), expiry_date=today + timedelta(days=180), storage_condition="Ambient", cost_per_kg=125.0),
    ]
    db.add_all(inv_items)
    db.commit()

    # 7. Production & Consumption Records for the past 5 days
    for day_offset in range(5, 0, -1):
        rec_date = today - timedelta(days=day_offset)
        prod = FoodProduction(
            kitchen_id=k1.id,
            date=rec_date,
            meal_type="Lunch",
            recipe_name="Dal Makhani, Jeera Rice & Mix Sabzi",
            planned_quantity_portions=550,
            actual_quantity_portions=540,
            raw_material_used_kg=215.0,
            shelf_life_hours=6.0,
            is_redistribution_eligible=True
        )
        cons = FoodConsumption(
            kitchen_id=k1.id,
            date=rec_date,
            meal_type="Lunch",
            registered_attendance=520,
            actual_diners=508,
            total_portions_served=508,
            plate_waste_kg=9.2,
            service_waste_kg=4.8,
            kitchen_notes="Normal dining throughput."
        )
        db.add_all([prod, cons])

    db.commit()

    # 8. Food Surplus & Food Donations
    surplus1 = FoodSurplus(
        kitchen_id=k1.id,
        date=today,
        meal_type="Lunch",
        item_name="Steamed Vegetable Pulao & Rajma Curry",
        surplus_portions=45,
        surplus_kg=18.0,
        cause_of_surplus="Afternoon attendance lower than forecasted due to technical fest",
        is_listed_for_donation=True
    )
    surplus2 = FoodSurplus(
        kitchen_id=k2.id,
        date=today,
        meal_type="High Tea",
        item_name="Assorted Gourmet Sandwiches & Baked Buns",
        surplus_portions=70,
        surplus_kg=22.5,
        cause_of_surplus="Corporate seminar concluded early",
        is_listed_for_donation=True
    )
    db.add_all([surplus1, surplus2])
    db.commit()

    now = datetime.utcnow()
    d1 = FoodDonation(
        donation_code="FD-10492",
        kitchen_id=k1.id,
        surplus_id=surplus1.id,
        title="Nutritious Vegetable Pulao & Warm Rajma Curry",
        food_category="Cooked Meals",
        quantity_kg=18.0,
        portions=45,
        preparation_time=now - timedelta(hours=1, minutes=30),
        safe_use_deadline=now + timedelta(hours=3, minutes=30),
        storage_condition="Heated Insulated Containers (>60°C)",
        packaging_type="Food-grade stainless steel pans with sealed lids",
        pickup_address=i1.address,
        pickup_latitude=i1.latitude,
        pickup_longitude=i1.longitude,
        special_instructions="FSSAI hygiene verified. Enter via Campus Gate 2 loading dock.",
        status=DonationStatus.AVAILABLE,
        safety_verified=True
    )
    d2 = FoodDonation(
        donation_code="FD-10488",
        kitchen_id=k2.id,
        surplus_id=surplus2.id,
        title="Assorted Club Sandwiches & Baked Pastries",
        food_category="Bakery",
        quantity_kg=22.5,
        portions=70,
        preparation_time=now - timedelta(hours=2),
        safe_use_deadline=now + timedelta(hours=4),
        storage_condition="Chilled Storage (< 5°C)",
        packaging_type="Hygienically sealed eco-friendly meal boxes",
        pickup_address=i2.address,
        pickup_latitude=i2.latitude,
        pickup_longitude=i2.longitude,
        special_instructions="Individual portion packaging ready for direct distribution.",
        status=DonationStatus.ACCEPTED,
        safety_verified=True,
        accepted_ngo_id=ngo1.id
    )
    db.add_all([d1, d2])
    db.commit()

    # Tracking for accepted donation
    trk = DeliveryTracking(
        donation_id=d2.id,
        current_status=DonationStatus.ACCEPTED,
        current_latitude=28.6360,
        current_longitude=77.2150,
        eta_minutes=25,
        distance_remaining_km=4.8,
        temperature_logged_celsius=4.2
    )
    ps = PickupSchedule(
        donation_id=d2.id,
        vehicle_type="Refrigerated Van Alpha",
        driver_name="Ramesh Kumar (Volunteer Lead)",
        driver_phone="+91 98112 99887",
        scheduled_pickup_time=now + timedelta(minutes=20),
        estimated_delivery_time=now + timedelta(minutes=50)
    )
    db.add_all([trk, ps])
    db.commit()

    # 9. Food Processing Production Records & Machine Telemetry
    p_rec1 = ProductionRecord(
        unit_id=p1.id,
        batch_number="BATCH-AGRO-26-081",
        product_name="Canned Diced Tomatoes (400g)",
        date=today,
        raw_material_input_kg=4500.0,
        finished_product_output_kg=4140.0,
        material_loss_kg=360.0,
        production_efficiency_pct=92.0,
        planned_production_kg=4200.0,
        variance_pct=-1.4
    )
    p_rec2 = ProductionRecord(
        unit_id=p1.id,
        batch_number="BATCH-AGRO-26-080",
        product_name="Mango Pulp Concentrate",
        date=today - timedelta(days=1),
        raw_material_input_kg=6000.0,
        finished_product_output_kg=5340.0,
        material_loss_kg=660.0,
        production_efficiency_pct=89.0,
        planned_production_kg=5400.0,
        variance_pct=-1.1
    )
    db.add_all([p_rec1, p_rec2])

    m1 = MachineMonitoring(unit_id=p1.id, machine_name="Continuous Steam Peeler", machine_code="PEELER-01", status="OPERATIONAL", operating_hours=7.5, downtime_minutes=15.0, temperature_celsius=105.0, vibration_mm_s=1.1, pressure_bar=4.2)
    m2 = MachineMonitoring(unit_id=p1.id, machine_name="Industrial Canning Retort", machine_code="RETORT-02", status="OPERATIONAL", operating_hours=8.0, downtime_minutes=0.0, temperature_celsius=121.5, vibration_mm_s=0.8, pressure_bar=2.8)
    m3 = MachineMonitoring(unit_id=p1.id, machine_name="Automatic Seamer & Capper", machine_code="SEAMER-03", status="OPERATIONAL", operating_hours=6.8, downtime_minutes=25.0, downtime_reason="Can jam cleared in 25 min", temperature_celsius=48.0, vibration_mm_s=2.2, pressure_bar=3.1)
    db.add_all([m1, m2, m3])

    e1 = EnergyConsumption(unit_id=p1.id, date=today, shift="Morning Shift", electricity_kwh=1250.0, water_liters=6800.0, fuel_liters=120.0, specific_energy_kwh_per_kg=0.302, is_abnormal_consumption=False)
    e2 = EnergyConsumption(unit_id=p1.id, date=today - timedelta(days=1), shift="Morning Shift", electricity_kwh=1310.0, water_liters=7100.0, fuel_liters=135.0, specific_energy_kwh_per_kg=0.316, is_abnormal_consumption=False)
    db.add_all([e1, e2])
    db.commit()

    print("Database seeding completed successfully!")
    db.close()

if __name__ == "__main__":
    seed()
