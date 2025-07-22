import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ingredient import Ingredient
from app.models.meal import Meal
from app.models.meal_ingredient import MealIngredient


def clear_data(db: Session):
    db.query(MealIngredient).delete()
    db.query(Meal).delete()
    db.query(Ingredient).delete()
    db.commit()
    print("✅ Cleared existing data.")


def seed_ingredients(db: Session) -> dict[str, Ingredient]:
    ingredients_data = [
        {"name": "Chicken Breast", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0},
        {"name": "Brown Rice", "calories": 111, "protein": 2.6, "fat": 0.9, "carbs": 23},
        {"name": "Broccoli", "calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 6.6},
        {"name": "Avocado", "calories": 160, "protein": 2, "fat": 15, "carbs": 9},
        {"name": "Greek Yogurt", "calories": 59, "protein": 10, "fat": 2, "carbs": 3.6},
        {"name": "Egg", "calories": 155, "protein": 13, "fat": 11, "carbs": 1.1},
        {"name": "Quinoa", "calories": 120, "protein": 4.1, "fat": 1.9, "carbs": 21.3},
        {"name": "Salmon", "calories": 208, "protein": 20, "fat": 13, "carbs": 0},
    ]

    ingredients = []
    for data in ingredients_data:
        ingredient = Ingredient(**data)
        db.add(ingredient)
        ingredients.append(ingredient)

    db.commit()
    print(f"✅ Seeded {len(ingredients)} ingredients.")
    return {i.name: i for i in ingredients}


def calculate_macros(ingredient: Ingredient, grams: float) -> dict:
    ratio = grams / 100.0
    return {
        "calories": ingredient.calories * ratio,
        "protein": ingredient.protein * ratio,
        "fat": ingredient.fat * ratio,
        "carbs": ingredient.carbs * ratio,
    }


def seed_meals(db: Session, ingredients: dict[str, Ingredient]):
    meals_data = [
        {
            "name": "Bodybuilder Bowl",
            "components": [
                ("Chicken Breast", 150),
                ("Brown Rice", 100),
                ("Broccoli", 80),
                ("Avocado", 50)
            ]
        },
        {
            "name": "Protein Breakfast",
            "components": [
                ("Egg", 100),
                ("Greek Yogurt", 150),
                ("Avocado", 30)
            ]
        },
        {
            "name": "Salmon Quinoa Bowl",
            "components": [
                ("Salmon", 120),
                ("Quinoa", 100),
                ("Broccoli", 60)
            ]
        },
    ]

    for meal_data in meals_data:
        macros = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}

        ingredient_links = []
        for ing_name, grams in meal_data["components"]:
            ingredient = ingredients.get(ing_name)
            if ingredient:
                ing_macros = calculate_macros(ingredient, grams)
                for key in macros:
                    macros[key] += ing_macros[key]

                link = MealIngredient(
                    ingredient_id=ingredient.id,
                    amount_grams=grams
                )
                ingredient_links.append(link)

        # Round macros for storage
        meal = Meal(
            name=meal_data["name"],
            calories=round(macros["calories"], 2),
            protein=round(macros["protein"], 2),
            fat=round(macros["fat"], 2),
            carbs=round(macros["carbs"], 2),
            ingredient_links=ingredient_links
        )
        db.add(meal)

        print(f"📦 {meal.name} → {round(macros['calories'])} kcal "
              f"({round(macros['protein'],1)}P / {round(macros['fat'],1)}F / {round(macros['carbs'],1)}C)")

    db.commit()
    print(f"✅ Seeded {len(meals_data)} meals with nutrition and links.")


def main():
    db = SessionLocal()
    try:
        clear_data(db)
        ingredients = seed_ingredients(db)
        seed_meals(db, ingredients)
    finally:
        db.close()


if __name__ == "__main__":
    main()
