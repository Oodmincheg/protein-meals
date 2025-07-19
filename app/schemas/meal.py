from pydantic import BaseModel
from typing import Optional, List

from app.schemas.ingredient import IngredientOut

class MealSummary(BaseModel):
    id: int
    name: str
    ingredients: str
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float

class MealBase(BaseModel):
    name: str

class MealCreate(MealBase):
    pass

class MealUpdate(MealBase):
    pass

class MealOut(MealBase):
    id: int
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    allergens: Optional[str] = None

    class Config:
        from_attributes = True

class MealWithIngredients(BaseModel):
    id: int
    name: str
    ingredients: List[IngredientOut]

    class Config:
        from_attributes = True