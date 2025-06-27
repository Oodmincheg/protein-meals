from sqlalchemy import Column, Integer, String, Float, JSON, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    
    # Nutrition information
    total_protein = Column(Float, nullable=False)
    total_calories = Column(Float, nullable=False)
    total_carbs = Column(Float)
    total_fat = Column(Float)
    
    # Meal details
    prep_time_minutes = Column(Integer)
    cook_time_minutes = Column(Integer)
    servings = Column(Integer, default=1)
    
    # Categories and tags
    cuisine_type = Column(String(50))  # Mediterranean, Asian, American, etc.
    diet_tags = Column(JSON, default=list)  # ["vegetarian", "gluten-free", "dairy-free"]
    
    # Ingredients stored as JSON
    # Format: [{"name": "chicken breast", "amount": 150, "unit": "g", "protein": 46.5}, ...]
    ingredients = Column(JSON, nullable=False)
    
    # Instructions
    instructions = Column(JSON)  # ["Step 1...", "Step 2...", ...]
    
    # Metadata
    ai_generated = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    popularity_score = Column(Integer, default=0)
    times_served = Column(Integer, default=0)
    
    # Image URL (optional)
    image_url = Column(String)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
