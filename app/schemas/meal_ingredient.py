from pydantic import BaseModel

class MealIngredientBase(BaseModel):
    ingredient_id: int
    amount_grams: float

class MealIngredientCreate(MealIngredientBase):
    meal_id: int

class MealIngredientUpdate(BaseModel):
    amount_grams: float

class MealIngredientOut(BaseModel):
    meal_id: int
    ingredient_id: int
    amount_grams: float

    class Config:
        from_attributes = True
