from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Numeric
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient
from app.schemas.meal import MealCreate, MealUpdate

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


def get_meal(db: Session, meal_id: int):
    return db.query(Meal).filter(Meal.id == meal_id).first()

def get_all_meals(db: Session):
    return db.query(Meal).order_by(Meal.id).all()

def create_meal(db: Session, meal: MealCreate):
    db_meal = Meal(**Ingredient.model_dump())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def update_meal(db: Session, meal_id: int, update: MealUpdate):
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        return None
    for field, value in update.dict().items():
        setattr(db_meal, field, value)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def delete_meal(db: Session, meal_id: int):
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        return None
    db.delete(db_meal)
    db.commit()
    return db_meal