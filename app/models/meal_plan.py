from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Date, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Plan details
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Meals organized by day and meal type
    # Format: {
    #   "2024-01-15": {
    #     "breakfast": [meal_id_1],
    #     "lunch": [meal_id_2],
    #     "dinner": [meal_id_3],
    #     "snack": [meal_id_4, meal_id_5]
    #   },
    #   ...
    # }
    meals_schedule = Column(JSON, nullable=False)
    
    # Summary stats
    total_meals = Column(Integer)
    avg_daily_protein = Column(Float)
    avg_daily_calories = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", backref="meal_plans")

class UserMealHistory(Base):
    __tablename__ = "user_meal_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    
    # When the meal was consumed
    consumed_date = Column(Date, nullable=False)
    meal_type = Column(String(50))  # breakfast, lunch, dinner, snack
    
    # User feedback
    rating = Column(Integer)  # 1-5 stars
    notes = Column(Text)
    completed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", backref="meal_history")
    meal = relationship("Meal", backref="consumption_history")
