from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class IngredientBase(BaseModel):
    name: str = Field(min_length=1)
    calories: float
    protein: float
    fat: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    # all optional for partial update
    name: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None

    model_config = ConfigDict(from_attributes=True, extra="forbid")

class IngredientOut(IngredientBase):
    id: int
