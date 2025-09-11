from pydantic import BaseModel, ConfigDict

class MealIngredientBase(BaseModel):
    ingredient_id: int
    amount_grams: float

    model_config = ConfigDict(from_attributes=True)

class MealIngredientCreate(MealIngredientBase):
    meal_id: int

class MealIngredientUpdate(BaseModel):
    amount_grams: float
    model_config = ConfigDict(from_attributes=True)

class MealIngredientOut(BaseModel):
    meal_id: int
    ingredient_id: int
    amount_grams: float

    model_config = ConfigDict(from_attributes=True)
