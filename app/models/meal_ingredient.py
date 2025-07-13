from sqlalchemy import Column, Integer, ForeignKey, Float
from app.database import Base

class MealIngredient(Base):
    __tablename__ = "meal_ingredient"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meal.id", ondelete="CASCADE"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.id", ondelete="CASCADE"))
    amount_grams = Column(Float, nullable=False)
