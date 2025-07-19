from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

MealIngredient = Table(
    "meal_ingredient",
    Base.metadata,
    Column("meal_id", Integer, ForeignKey("meal.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True)
)