from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class MealIngredient(Base):
    __tablename__ = "meal_ingredient"

    meal_id = Column(Integer, ForeignKey("meal.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    amount_grams = Column(Float, nullable=False)

    meal = relationship("Meal", back_populates="ingredient_links")
    ingredient = relationship("Ingredient", back_populates="meal_links")
