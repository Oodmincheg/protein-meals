from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate

def get_ingredient(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

def get_all_ingredients(db: Session):
    return db.query(Ingredient).order_by(Ingredient.id).all()

def create_ingredient(db: Session, ingredient: IngredientCreate):
    db_ingredient = Ingredient(**ingredient.model_dump())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def update_ingredient(db: Session, ingredient_id: int, update: IngredientUpdate):
    db_ingredient = get_ingredient(db, ingredient_id)
    if not db_ingredient:
        return None
    for field, value in update.model_dump().items():
        setattr(db_ingredient, field, value)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = get_ingredient(db, ingredient_id)
    if not db_ingredient:
        return None
    db.delete(db_ingredient)
    db.commit()
    return db_ingredient
