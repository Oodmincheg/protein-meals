from pydantic import BaseModel

class MealSummary(BaseModel):
    id: int
    name: str
    ingredients: str
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
