from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Profile information
    weight_kg = Column(Float)
    height_cm = Column(Float)
    activity_level = Column(String)  # sedentary, moderate, active, very_active
    fitness_goal = Column(String)  # maintain, lose_weight, gain_muscle
    
    # Preferences
    dietary_restrictions = Column(JSON, default=list)  # ["vegetarian", "gluten-free", etc.]
    excluded_ingredients = Column(JSON, default=list)  # ["peanuts", "shellfish", etc.]
    
    # Calculated fields
    daily_protein_goal = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
