from sqlalchemy.orm import Session
from app.models.meal_ingredient import MealIngredient
from app.schemas.meal_ingredient import MealIngredientCreate, MealIngredientUpdate

def get_meal_ingredient(db: Session, mi_id: int):
    return db.query(MealIngredient).filter(MealIngredient.id == mi_id).first()

def get_all_meal_ingredients(db: Session):
    return db.query(MealIngredient).order_by(MealIngredient.id).all()

def create_meal_ingredient(db: Session, data: MealIngredientCreate):
    db_item = MealIngredient(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_meal_ingredient(db: Session, mi_id: int, data: MealIngredientUpdate):
    db_item = get_meal_ingredient(db, mi_id)
    if not db_item:
        return None
    for key, value in data.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_meal_ingredient(db: Session, mi_id: int):
    db_item = get_meal_ingredient(db, mi_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
