# app/crud/meal_ingredient.py
from sqlalchemy.orm import Session
from app.models.meal_ingredient import MealIngredient
from app.schemas.meal_ingredient import MealIngredientCreate, MealIngredientUpdate

def create_meal_ingredient(db: Session, data: MealIngredientCreate):
    meal_ingredient = MealIngredient(**data.dict())
    db.add(meal_ingredient)
    db.commit()
    db.refresh(meal_ingredient)
    return meal_ingredient

def get_meal_ingredient(db: Session, meal_id: int, ingredient_id: int):
    return (
        db.query(MealIngredient)
        .filter(
            MealIngredient.meal_id == meal_id,
            MealIngredient.ingredient_id == ingredient_id
        )
        .first()
    )

def get_all_meal_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MealIngredient).offset(skip).limit(limit).all()

def update_meal_ingredient(db: Session, meal_id: int, ingredient_id: int, data: MealIngredientUpdate):
    meal_ingredient = get_meal_ingredient(db, meal_id, ingredient_id)
    if meal_ingredient:
        meal_ingredient.amount_grams = data.amount_grams
        db.commit()
        db.refresh(meal_ingredient)
    return meal_ingredient

def delete_meal_ingredient(db: Session, meal_id: int, ingredient_id: int):
    meal_ingredient = get_meal_ingredient(db, meal_id, ingredient_id)
    if meal_ingredient:
        db.delete(meal_ingredient)
        db.commit()
    return meal_ingredient
