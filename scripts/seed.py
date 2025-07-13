import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ingredient import Ingredient
from app.models.meal import Meal
from app.models.meal_ingredient import MealIngredient

def seed_ingredients(session: Session):
    ingredients_data = [
        {"name": "Chicken Breast", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0},
        {"name": "Brown Rice", "calories": 111, "protein": 2.6, "fat": 0.9, "carbs": 23},
        {"name": "Broccoli", "calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 6.6},
        {"name": "Salmon", "calories": 208, "protein": 20, "fat": 13, "carbs": 0},
        {"name": "Sweet Potato", "calories": 86, "protein": 1.6, "fat": 0.1, "carbs": 20},
        {"name": "Quinoa", "calories": 120, "protein": 4.1, "fat": 1.9, "carbs": 21.3},
        {"name": "Egg", "calories": 155, "protein": 13, "fat": 11, "carbs": 1.1},
        {"name": "Avocado", "calories": 160, "protein": 2, "fat": 15, "carbs": 9},
        {"name": "Tofu", "calories": 76, "protein": 8, "fat": 4.8, "carbs": 1.9},
        {"name": "Spinach", "calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6},
        {"name": "Ground Beef (85% lean)", "calories": 250, "protein": 26, "fat": 17, "carbs": 0},
        {"name": "Turkey Breast", "calories": 135, "protein": 30, "fat": 1, "carbs": 0},
        {"name": "Greek Yogurt (plain, 2%)", "calories": 59, "protein": 10, "fat": 2, "carbs": 3.6},
        {"name": "Almonds", "calories": 579, "protein": 21, "fat": 50, "carbs": 22},
        {"name": "Oats", "calories": 389, "protein": 17, "fat": 7, "carbs": 66},
        {"name": "Zucchini", "calories": 17, "protein": 1.2, "fat": 0.3, "carbs": 3.1},
        {"name": "Carrot", "calories": 41, "protein": 0.9, "fat": 0.2, "carbs": 10},
        {"name": "Cucumber", "calories": 16, "protein": 0.7, "fat": 0.1, "carbs": 3.6},
        {"name": "Red Bell Pepper", "calories": 31, "protein": 1, "fat": 0.3, "carbs": 6},
        {"name": "Green Peas", "calories": 81, "protein": 5, "fat": 0.4, "carbs": 14},
        {"name": "Corn", "calories": 86, "protein": 3.3, "fat": 1.2, "carbs": 19},
        {"name": "Lentils", "calories": 116, "protein": 9, "fat": 0.4, "carbs": 20},
        {"name": "Chickpeas", "calories": 164, "protein": 8.9, "fat": 2.6, "carbs": 27.4},
        {"name": "Black Beans", "calories": 132, "protein": 8.9, "fat": 0.5, "carbs": 23.7},
        {"name": "Kidney Beans", "calories": 127, "protein": 8.7, "fat": 0.5, "carbs": 22.8},
        {"name": "Cottage Cheese (2%)", "calories": 82, "protein": 11, "fat": 2.3, "carbs": 3.4},
        {"name": "Mozzarella (part-skim)", "calories": 280, "protein": 28, "fat": 17, "carbs": 3.1},
        {"name": "Parmesan", "calories": 431, "protein": 38, "fat": 29, "carbs": 4.1},
        {"name": "Cheddar", "calories": 403, "protein": 25, "fat": 33, "carbs": 1.3},
        {"name": "Whole Wheat Bread", "calories": 247, "protein": 13, "fat": 4.2, "carbs": 41},
        {"name": "Tortilla (whole grain)", "calories": 237, "protein": 8, "fat": 4.5, "carbs": 38},
        {"name": "Milk (2%)", "calories": 50, "protein": 3.4, "fat": 2, "carbs": 5},
        {"name": "Banana", "calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23},
        {"name": "Apple", "calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14},
        {"name": "Blueberries", "calories": 57, "protein": 0.7, "fat": 0.3, "carbs": 14},
        {"name": "Strawberries", "calories": 32, "protein": 0.7, "fat": 0.3, "carbs": 7.7},
        {"name": "Dates", "calories": 282, "protein": 2.5, "fat": 0.4, "carbs": 75},
        {"name": "Peanut Butter", "calories": 588, "protein": 25, "fat": 50, "carbs": 20},
        {"name": "Walnuts", "calories": 654, "protein": 15, "fat": 65, "carbs": 14},
        {"name": "Sunflower Seeds", "calories": 584, "protein": 20.8, "fat": 51.5, "carbs": 20},
        {"name": "Pumpkin Seeds", "calories": 446, "protein": 19, "fat": 19, "carbs": 54},
        {"name": "Coconut Milk", "calories": 230, "protein": 2.3, "fat": 24, "carbs": 6},
        {"name": "Protein Powder (whey)", "calories": 400, "protein": 80, "fat": 5, "carbs": 8},
        {"name": "Cocoa Powder", "calories": 228, "protein": 19.6, "fat": 13.7, "carbs": 57.9},
        {"name": "Olive Oil", "calories": 884, "protein": 0, "fat": 100, "carbs": 0},
        {"name": "Butter", "calories": 717, "protein": 0.9, "fat": 81, "carbs": 0.1},
        {"name": "Garlic", "calories": 149, "protein": 6.4, "fat": 0.5, "carbs": 33},
        {"name": "Onion", "calories": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3},
        {"name": "Tomato", "calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9},
        {"name": "Hummus", "calories": 166, "protein": 7.9, "fat": 9.6, "carbs": 14.3},
        {"name": "Pita Bread", "calories": 275, "protein": 9.1, "fat": 1.2, "carbs": 55}
    ]

    ingredients = []
    for data in ingredients_data:
        ingredient = Ingredient(**data)
        session.add(ingredient)
        ingredients.append(ingredient)

    session.commit()
    print(f"Seeded {len(ingredients)} ingredients.")

    return {i.name: i for i in ingredients}


def seed_meals(session: Session, ingredients: dict):
    meals = [
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
            "name": "Lean Chicken Wrap",
            "components": [
                ("Chicken Breast", 120),
                ("Spinach", 30),
                ("Sweet Potato", 100)
            ]
        },

        {"name": "Power Lentil Bowl", "components": [("Lentils", 100), ("Spinach", 40), ("Avocado", 50)]},
        {"name": "Protein Oats", "components": [("Oats", 60), ("Milk (2%)", 200), ("Protein Powder (whey)", 30)]},
        {"name": "Vegan Wrap", "components": [("Hummus", 50), ("Cucumber", 50), ("Tomato", 50), ("Tortilla (whole grain)", 60)]},
        {"name": "Peanut Banana Shake", "components": [("Banana", 100), ("Peanut Butter", 30), ("Milk (2%)", 200)]},
        {"name": "Turkey Quinoa Salad", "components": [("Turkey Breast", 100), ("Quinoa", 80), ("Red Bell Pepper", 50)]},
        {"name": "Greek Bowl", "components": [("Greek Yogurt (plain, 2%)", 150), ("Cucumber", 40), ("Olive Oil", 10)]},
        {"name": "Egg & Avocado Toast", "components": [("Egg", 2 * 50), ("Whole Wheat Bread", 60), ("Avocado", 50)]},
        {"name": "Tofu Stir Fry", "components": [("Tofu", 100), ("Zucchini", 60), ("Onion", 40), ("Olive Oil", 10)]},
    ]

    for meal_data in meals:
        meal = Meal(name=meal_data["name"])
        session.add(meal)
        session.flush()  # To get meal.id

        for ing_name, amount in meal_data["components"]:
            ingredient = ingredients.get(ing_name)
            if ingredient:
                link = MealIngredient(
                    meal_id=meal.id,
                    ingredient_id=ingredient.id,
                    amount_grams=amount
                )
                session.add(link)

    session.commit()
    print(f"Seeded {len(meals)} meals with ingredients.")


if __name__ == "__main__":
    db = SessionLocal()

    # Wipe existing data
    db.query(MealIngredient).delete()
    db.query(Meal).delete()
    db.query(Ingredient).delete()
    db.commit()
    print("✅ Cleared existing ingredients, meals, and relations.")

    try:
        ingredients_dict = seed_ingredients(db)
        seed_meals(db, ingredients_dict)
    finally:
        db.close()
