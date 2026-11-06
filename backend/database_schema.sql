-- ==============================================================================
-- FoodWise AI - Smart Food Waste Management & Redistribution Ecosystem
-- MoFPI Problem Statement 26234
-- Relational Database Schema DDL (PostgreSQL)
-- ==============================================================================

-- 1. Create Enums
CREATE TYPE user_role_enum AS ENUM ('ADMIN', 'KITCHEN_MANAGER', 'PROCESSING_MANAGER', 'NGO');
CREATE TYPE donation_status_enum AS ENUM ('AVAILABLE', 'ACCEPTED', 'PICKUP_SCHEDULED', 'COLLECTED', 'DELIVERED', 'COMPLETED', 'REJECTED', 'CANCELLED');

-- 2. Organizations & Entities
CREATE TABLE IF NOT EXISTS institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL DEFAULT 'New Delhi',
    state VARCHAR(100) NOT NULL DEFAULT 'Delhi',
    latitude DOUBLE PRECISION NOT NULL DEFAULT 28.6139,
    longitude DOUBLE PRECISION NOT NULL DEFAULT 77.2090,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(50) NOT NULL,
    fssai_license VARCHAR(100),
    is_verified BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kitchens (
    id SERIAL PRIMARY KEY,
    institution_id INTEGER NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    daily_capacity_meals INTEGER DEFAULT 500,
    service_type VARCHAR(100) DEFAULT 'Buffet & Meal Trays',
    storage_capacity_kg DOUBLE PRECISION DEFAULT 1000.0,
    has_cold_storage BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS food_processing_units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    daily_processing_capacity_tons DOUBLE PRECISION DEFAULT 10.0,
    latitude DOUBLE PRECISION NOT NULL DEFAULT 28.5355,
    longitude DOUBLE PRECISION NOT NULL DEFAULT 77.3910,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ngos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL DEFAULT 'New Delhi',
    latitude DOUBLE PRECISION NOT NULL DEFAULT 28.6289,
    longitude DOUBLE PRECISION NOT NULL DEFAULT 77.2065,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(50) NOT NULL,
    daily_meals_capacity INTEGER DEFAULT 300,
    preferred_food_categories VARCHAR(255) DEFAULT 'Cooked Meals, Breads, Fruits, Packaged Foods',
    has_refrigerated_transport BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Users Table (Role-based access control)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'KITCHEN_MANAGER',
    phone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    institution_id INTEGER REFERENCES institutions(id) ON DELETE SET NULL,
    kitchen_id INTEGER REFERENCES kitchens(id) ON DELETE SET NULL,
    processing_unit_id INTEGER REFERENCES food_processing_units(id) ON DELETE SET NULL,
    ngo_id INTEGER REFERENCES ngos(id) ON DELETE SET NULL
);

-- 4. Kitchen Operations: Inventory, Production, Consumption, Demand Forecasting
CREATE TABLE IF NOT EXISTS food_inventory (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    current_stock_kg DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    unit VARCHAR(50) NOT NULL DEFAULT 'kg',
    reorder_level_kg DOUBLE PRECISION DEFAULT 10.0,
    purchase_date DATE DEFAULT CURRENT_DATE,
    expiry_date DATE NOT NULL,
    storage_condition VARCHAR(100) DEFAULT 'Ambient (Dry Storage)',
    cost_per_kg DOUBLE PRECISION DEFAULT 50.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS food_production (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    meal_type VARCHAR(50) NOT NULL,
    recipe_name VARCHAR(255) NOT NULL,
    planned_quantity_portions INTEGER NOT NULL,
    actual_quantity_portions INTEGER NOT NULL,
    raw_material_used_kg DOUBLE PRECISION DEFAULT 0.0,
    preparation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    shelf_life_hours DOUBLE PRECISION DEFAULT 6.0,
    is_redistribution_eligible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS food_consumption (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    meal_type VARCHAR(50) NOT NULL,
    registered_attendance INTEGER NOT NULL,
    actual_diners INTEGER NOT NULL,
    total_portions_served INTEGER NOT NULL,
    plate_waste_kg DOUBLE PRECISION DEFAULT 0.0,
    service_waste_kg DOUBLE PRECISION DEFAULT 0.0,
    kitchen_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demand_predictions (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    target_date DATE NOT NULL,
    meal_type VARCHAR(50) NOT NULL,
    forecasted_attendance INTEGER NOT NULL,
    predicted_demand_portions INTEGER NOT NULL,
    recommended_production_portions INTEGER NOT NULL,
    expected_surplus_portions INTEGER DEFAULT 0,
    confidence_interval_low INTEGER DEFAULT 0,
    confidence_interval_high INTEGER DEFAULT 0,
    features_used JSONB,
    model_version VARCHAR(50) DEFAULT 'RandomForest_v1.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS food_surplus (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    meal_type VARCHAR(50) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    surplus_portions INTEGER NOT NULL,
    surplus_kg DOUBLE PRECISION NOT NULL,
    cause_of_surplus VARCHAR(255) DEFAULT 'Overestimation of attendance',
    is_listed_for_donation BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Food Quality Assessment & IoT Telemetry
CREATE TABLE IF NOT EXISTS food_quality_assessments (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER REFERENCES kitchens(id) ON DELETE CASCADE,
    item_name VARCHAR(255) NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    visual_quality_category VARCHAR(100) NOT NULL,
    confidence_score DOUBLE PRECISION NOT NULL,
    detected_features JSONB,
    requires_human_inspection BOOLEAN DEFAULT FALSE,
    human_verifier_notes TEXT,
    is_redistribution_approved BOOLEAN DEFAULT TRUE,
    safety_disclaimer VARCHAR(500),
    assessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS iot_sensor_readings (
    id SERIAL PRIMARY KEY,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    sensor_id VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    storage_area VARCHAR(100) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20) NOT NULL,
    threshold_min DOUBLE PRECISION,
    threshold_max DOUBLE PRECISION,
    is_anomaly BOOLEAN DEFAULT FALSE,
    alert_triggered BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Redistribution & Logistics Marketplace
CREATE TABLE IF NOT EXISTS food_donations (
    id SERIAL PRIMARY KEY,
    donation_code VARCHAR(50) UNIQUE NOT NULL,
    kitchen_id INTEGER NOT NULL REFERENCES kitchens(id) ON DELETE CASCADE,
    surplus_id INTEGER REFERENCES food_surplus(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    food_category VARCHAR(100) NOT NULL,
    quantity_kg DOUBLE PRECISION NOT NULL,
    portions INTEGER NOT NULL,
    preparation_time TIMESTAMP WITH TIME ZONE NOT NULL,
    safe_use_deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    storage_condition VARCHAR(100) DEFAULT 'Heated Container / Hot Holding (>60°C)',
    packaging_type VARCHAR(100) DEFAULT 'Food-grade Insulated Cans',
    pickup_address TEXT NOT NULL,
    pickup_latitude DOUBLE PRECISION NOT NULL,
    pickup_longitude DOUBLE PRECISION NOT NULL,
    special_instructions TEXT,
    status donation_status_enum NOT NULL DEFAULT 'AVAILABLE',
    safety_verified BOOLEAN DEFAULT TRUE,
    accepted_ngo_id INTEGER REFERENCES ngos(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS donation_requests (
    id SERIAL PRIMARY KEY,
    donation_id INTEGER NOT NULL REFERENCES food_donations(id) ON DELETE CASCADE,
    ngo_id INTEGER NOT NULL REFERENCES ngos(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'PENDING',
    estimated_arrival_minutes INTEGER DEFAULT 30,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pickup_schedules (
    id SERIAL PRIMARY KEY,
    donation_id INTEGER UNIQUE NOT NULL REFERENCES food_donations(id) ON DELETE CASCADE,
    vehicle_type VARCHAR(100) DEFAULT 'Refrigerated Van',
    driver_name VARCHAR(255) DEFAULT 'Volunteer Team Alpha',
    driver_phone VARCHAR(50) DEFAULT '+91 98765 43210',
    scheduled_pickup_time TIMESTAMP WITH TIME ZONE NOT NULL,
    estimated_delivery_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS delivery_tracking (
    id SERIAL PRIMARY KEY,
    donation_id INTEGER UNIQUE NOT NULL REFERENCES food_donations(id) ON DELETE CASCADE,
    current_status donation_status_enum DEFAULT 'AVAILABLE',
    current_latitude DOUBLE PRECISION,
    current_longitude DOUBLE PRECISION,
    route_waypoints JSONB,
    eta_minutes INTEGER DEFAULT 25,
    distance_remaining_km DOUBLE PRECISION DEFAULT 5.2,
    temperature_logged_celsius DOUBLE PRECISION DEFAULT 4.0,
    delivered_at TIMESTAMP WITH TIME ZONE,
    receiver_signature_name VARCHAR(255),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Industrial Food Processing Unit Monitoring
CREATE TABLE IF NOT EXISTS production_records (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES food_processing_units(id) ON DELETE CASCADE,
    batch_number VARCHAR(100) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    raw_material_input_kg DOUBLE PRECISION NOT NULL,
    finished_product_output_kg DOUBLE PRECISION NOT NULL,
    material_loss_kg DOUBLE PRECISION NOT NULL,
    production_efficiency_pct DOUBLE PRECISION NOT NULL,
    planned_production_kg DOUBLE PRECISION NOT NULL,
    variance_pct DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS machine_monitoring (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES food_processing_units(id) ON DELETE CASCADE,
    machine_name VARCHAR(255) NOT NULL,
    machine_code VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'OPERATIONAL',
    operating_hours DOUBLE PRECISION DEFAULT 8.0,
    downtime_minutes DOUBLE PRECISION DEFAULT 0.0,
    downtime_reason VARCHAR(255),
    temperature_celsius DOUBLE PRECISION DEFAULT 75.0,
    vibration_mm_s DOUBLE PRECISION DEFAULT 1.2,
    pressure_bar DOUBLE PRECISION DEFAULT 3.5,
    maintenance_due_date DATE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS energy_consumption (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER NOT NULL REFERENCES food_processing_units(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    shift VARCHAR(50) DEFAULT 'Morning Shift',
    electricity_kwh DOUBLE PRECISION NOT NULL,
    water_liters DOUBLE PRECISION NOT NULL,
    fuel_liters DOUBLE PRECISION DEFAULT 0.0,
    specific_energy_kwh_per_kg DOUBLE PRECISION NOT NULL,
    is_abnormal_consumption BOOLEAN DEFAULT FALSE,
    alert_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Analytics & Sustainability Reports
CREATE TABLE IF NOT EXISTS waste_analytics (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    item_category VARCHAR(100) NOT NULL,
    waste_kg DOUBLE PRECISION NOT NULL,
    waste_cost_inr DOUBLE PRECISION NOT NULL,
    primary_cause VARCHAR(255) NOT NULL,
    is_anomaly BOOLEAN DEFAULT FALSE,
    anomaly_score DOUBLE PRECISION DEFAULT 0.0,
    ai_recommendation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sustainability_reports (
    id SERIAL PRIMARY KEY,
    report_period VARCHAR(50) NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total_food_waste_prevented_kg DOUBLE PRECISION NOT NULL,
    total_food_redistributed_kg DOUBLE PRECISION NOT NULL,
    meals_supported_count INTEGER NOT NULL,
    carbon_emissions_avoided_kg_co2e DOUBLE PRECISION NOT NULL,
    water_saved_liters DOUBLE PRECISION NOT NULL,
    energy_saved_kwh DOUBLE PRECISION NOT NULL,
    institutional_waste_reduction_pct DOUBLE PRECISION DEFAULT 24.5,
    active_ngos_count INTEGER DEFAULT 12,
    active_institutions_count INTEGER DEFAULT 8,
    summary_notes TEXT
);

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'INFO',
    is_read BOOLEAN DEFAULT FALSE,
    related_link VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_inventory_expiry ON food_inventory(expiry_date);
CREATE INDEX IF NOT EXISTS idx_donations_status ON food_donations(status);
CREATE INDEX IF NOT EXISTS idx_donations_deadline ON food_donations(safe_use_deadline);
CREATE INDEX IF NOT EXISTS idx_iot_timestamp ON iot_sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_production_batch ON production_records(batch_number);
