from sqlalchemy.orm import Session
from app.models.meal_ingredient import MealIngredient
from app.schemas.meal_ingredient import MealIngredientCreate, MealIngredientUpdate

def add_meal_ingredient(db: Session, data: MealIngredientCreate):
    link = MealIngredient(**data.dict())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def get_meal_ingredient(db: Session, meal_id: int, ingredient_id: int):
    return db.query(MealIngredient).filter_by(meal_id=meal_id, ingredient_id=ingredient_id).first()

def update_meal_ingredient(db: Session, meal_id: int, ingredient_id: int, data: MealIngredientUpdate):
    link = get_meal_ingredient(db, meal_id, ingredient_id)
    if not link:
        return None
    link.amount_grams = data.amount_grams
    db.commit()
    db.refresh(link)
    return link

def delete_meal_ingredient(db: Session, meal_id: int, ingredient_id: int):
    link = get_meal_ingredient(db, meal_id, ingredient_id)
    if not link:
        return None
    db.delete(link)
    db.commit()
    return link
