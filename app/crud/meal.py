from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Numeric
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient

def get_meal_summaries(db: Session):
    return (
        db.query(
            Meal.id.label("id"),
            Meal.name.label("name"),
            func.string_agg(Ingredient.name, ', ').label("ingredients"),
            func.round(
                cast(
                    func.sum(Ingredient.calories * MealIngredient.amount_grams / 100),
                    Numeric
                ), 1
            ).label("total_calories"),
            func.round(
                cast(
                    func.sum(Ingredient.protein * MealIngredient.amount_grams / 100),
                    Numeric
                ), 1
            ).label("total_protein"),
            func.round(
                cast(
                    func.sum(Ingredient.fat * MealIngredient.amount_grams / 100),
                    Numeric
                ), 1
            ).label("total_fat"),
            func.round(
                cast(
                    func.sum(Ingredient.carbs * MealIngredient.amount_grams / 100),
                    Numeric
                ), 1
            ).label("total_carbs"),
        )
        .join(MealIngredient, Meal.id == MealIngredient.meal_id)
        .join(Ingredient, Ingredient.id == MealIngredient.ingredient_id)
        .group_by(Meal.id, Meal.name)
        .order_by(Meal.id)
        .all()
    )
