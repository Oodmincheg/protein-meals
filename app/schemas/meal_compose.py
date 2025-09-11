# app/schemas/meal_compose.py
from typing import List
from pydantic import BaseModel, Field, ConfigDict, AliasChoices

class MealIngredientInput(BaseModel):
    ingredient_id: int
    amount_grams: float = Field(gt=0, description="Amount in grams")

class ComposeMealRequest(BaseModel):
    name: str = Field(min_length=1)
    # Accept payloads that use either "items" (new) or "ingredients" (legacy)
    items: List[MealIngredientInput] = Field(
        ...,
        min_length=1,
        validation_alias=AliasChoices("items", "ingredients"),
    )

    model_config = ConfigDict(from_attributes=True)

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
    calories: float
    protein: float
    fat: float
    carbs: float
    ingredients: List[MealIngredientContribution]

    model_config = ConfigDict(from_attributes=True)
