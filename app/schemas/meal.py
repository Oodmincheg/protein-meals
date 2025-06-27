from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class IngredientItem(BaseModel):
    name: str
    amount: float
    unit: str
    protein: Optional[float] = None

class MealBase(BaseModel):
    name: str
    description: Optional[str] = None
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    total_protein: float = Field(..., ge=0)
    total_calories: float = Field(..., ge=0)
    total_carbs: Optional[float] = Field(None, ge=0)
    total_fat: Optional[float] = Field(None, ge=0)
    prep_time_minutes: Optional[int] = Field(None, ge=0)
    cook_time_minutes: Optional[int] = Field(None, ge=0)
    servings: int = Field(1, ge=1)
    cuisine_type: Optional[str] = None
    diet_tags: List[str] = []
    ingredients: List[IngredientItem]
    instructions: Optional[List[str]] = []
    image_url: Optional[str] = None

class MealCreate(MealBase):
    pass

class MealResponse(MealBase):
    id: int
    verified: bool
    popularity_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True
