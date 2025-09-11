# app/schemas/meal.py
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

# If IngredientOut lives in app/schemas/ingredient.py, import it:
from app.schemas.ingredient import IngredientOut


class MealBase(BaseModel):
    name: str = Field(min_length=1)
    calories: float
    protein: float
    fat: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    name: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class MealOut(MealBase):
    id: int


class MealSummary(BaseModel):
    """Row for meals summary table."""
    id: int
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)


class MealWithIngredients(MealOut):
    """Meal + resolved ingredients list."""
    # Your Meal model defines @property ingredients -> [Ingredient] via relationship
    ingredients: List[IngredientOut] = []

    model_config = ConfigDict(from_attributes=True)
