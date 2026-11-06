from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class FoodInventory(Base):
    __tablename__ = "food_inventory"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # Grains, Dairy, Vegetables, Meat/Protein, Spices, Bakery
    current_stock_kg = Column(Float, nullable=False, default=0.0)
    unit = Column(String(50), nullable=False, default="kg")
    reorder_level_kg = Column(Float, default=10.0)
    purchase_date = Column(Date, default=date.today)
    expiry_date = Column(Date, nullable=False)
    storage_condition = Column(String(100), default="Ambient (Dry Storage)")  # Cold Storage, Freezer, Ambient
    cost_per_kg = Column(Float, default=50.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    kitchen = relationship("Kitchen", back_populates="inventory")

class FoodProduction(Base):
    __tablename__ = "food_production"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    meal_type = Column(String(50), nullable=False)  # Breakfast, Lunch, Dinner, High Tea
    recipe_name = Column(String(255), nullable=False)
    planned_quantity_portions = Column(Integer, nullable=False)
    actual_quantity_portions = Column(Integer, nullable=False)
    raw_material_used_kg = Column(Float, default=0.0)
    preparation_time = Column(DateTime, default=datetime.utcnow)
    shelf_life_hours = Column(Float, default=6.0)
    is_redistribution_eligible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    kitchen = relationship("Kitchen", back_populates="productions")

class FoodConsumption(Base):
    __tablename__ = "food_consumption"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    meal_type = Column(String(50), nullable=False)
    registered_attendance = Column(Integer, nullable=False)
    actual_diners = Column(Integer, nullable=False)
    total_portions_served = Column(Integer, nullable=False)
    plate_waste_kg = Column(Float, default=0.0)
    service_waste_kg = Column(Float, default=0.0)
    kitchen_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    kitchen = relationship("Kitchen", back_populates="consumptions")

class DemandPrediction(Base):
    __tablename__ = "demand_predictions"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    target_date = Column(Date, nullable=False)
    meal_type = Column(String(50), nullable=False)  # Lunch, Dinner, Breakfast
    forecasted_attendance = Column(Integer, nullable=False)
    predicted_demand_portions = Column(Integer, nullable=False)
    recommended_production_portions = Column(Integer, nullable=False)
    expected_surplus_portions = Column(Integer, default=0)
    confidence_interval_low = Column(Integer, default=0)
    confidence_interval_high = Column(Integer, default=0)
    features_used = Column(JSON, nullable=True)  # day_of_week, is_holiday, weather, past_trend
    model_version = Column(String(50), default="RandomForest_v1.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    kitchen = relationship("Kitchen", back_populates="predictions")

class FoodSurplus(Base):
    __tablename__ = "food_surplus"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    meal_type = Column(String(50), nullable=False)
    item_name = Column(String(255), nullable=False)
    surplus_portions = Column(Integer, nullable=False)
    surplus_kg = Column(Float, nullable=False)
    cause_of_surplus = Column(String(255), default="Overestimation of attendance")
    is_listed_for_donation = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    kitchen = relationship("Kitchen", back_populates="surpluses")
    donation = relationship("FoodDonation", back_populates="surplus_record", uselist=False)
