from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    pass

class IngredientOut(BaseModel):
    id: int
    name: str
    protein: float
    fat: float
    carbs: float
    allergens: str | None = None

    class Config:
        from_attributes = True