from pydantic import BaseModel
from typing import Optional

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

    class Config:
        from_attributes = True