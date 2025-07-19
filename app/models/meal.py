from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.meal_ingredient import MealIngredient

class Meal(Base):
    __tablename__ = "meal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    ingredients = relationship(
        "Ingredient",
        secondary=MealIngredient,
        back_populates="meals"
    )
