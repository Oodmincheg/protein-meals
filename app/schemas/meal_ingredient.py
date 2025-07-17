from pydantic import BaseModel
from typing import Optional

class MealIngredientBase(BaseModel):
    meal_id: int
    ingredient_id: int
    amount_grams: float

class MealIngredientCreate(MealIngredientBase):
    pass

class MealIngredientUpdate(MealIngredientBase):
    pass

class MealIngredientOut(MealIngredientBase):
    id: int

    class Config:
        from_attributes = True
