from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.meal_ingredient import MealIngredient

class Meal(Base):
    __tablename__ = "meal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)

    ingredient_links = relationship("MealIngredient", back_populates="meal", cascade="all, delete-orphan")

    @property
    def ingredients(self):
        return [link.ingredient for link in self.ingredient_links]
