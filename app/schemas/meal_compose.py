from typing import List, Optional
from pydantic import BaseModel, Field, conlist
from pydantic import ConfigDict  # v2-style config

class MealIngredientInput(BaseModel):
    ingredient_id: int
    amount_grams: float = Field(gt=0, description="Amount in grams for this ingredient")

class ComposeMealRequest(BaseModel):
    name: str = Field(min_length=1)
    allergens: Optional[str] = None
    items: List[MealIngredientInput] = Field(min_length=1)

class MealIngredientContribution(BaseModel):
    ingredient_id: int
    ingredient_name: str
    amount_grams: float
    calories: float
    protein: float
    fat: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)

class ComposeMealResponse(BaseModel):
    id: int
    name: str
    allergens: Optional[str] = None
    calories: float
    protein: float
    fat: float
    carbs: float
    ingredients: List[MealIngredientContribution]

    model_config = ConfigDict(from_attributes=True)
