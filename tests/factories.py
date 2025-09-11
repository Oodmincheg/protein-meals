# tests/factories.py
from app.models.ingredient import Ingredient
from app.models.meal import Meal

def make_ingredient(**kwargs):
    # Defaults are per 100g
    defaults = dict(
        name="Test Ingredient",
        calories=100.0,
        protein=10.0,
        fat=5.0,
        carbs=8.0,
    )
    defaults.update(kwargs)
    return Ingredient(**defaults)

def make_meal(**kwargs):
    defaults = dict(
        name="Test Meal",
        calories=0.0,
        protein=0.0,
        fat=0.0,
        carbs=0.0,
    )
    defaults.update(kwargs)
    return Meal(**defaults)
