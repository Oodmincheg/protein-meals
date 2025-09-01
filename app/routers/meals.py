from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.crud.meal import get_meal_summaries
from app.schemas.meal import MealSummary, MealCreate, MealUpdate, MealOut, MealWithIngredients
from app.crud import meal as crud
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient


router = APIRouter(prefix="/meals", tags=["meals"])

# JSON API endpoints
@router.get("/summary", response_model=List[MealSummary])
def read_meal_summaries(db: Session = Depends(get_db)):
    results = get_meal_summaries(db)
    return [dict(row._mapping) for row in results]

@router.get("/filter-by-ingredient", response_model=List[MealWithIngredients])
def filter_meals_by_ingredient(ingredient_name: str, db: Session = Depends(get_db)):
    meals = (
        db.query(Meal)
        .join(Meal.ingredient_links)
        .join(MealIngredient.ingredient)
        .filter(func.lower(Ingredient.name).like(f"%{ingredient_name.lower()}%"))
        .options(joinedload(Meal.ingredient_links).joinedload(MealIngredient.ingredient))
        .distinct()
        .all()
    )
    return meals

@router.post("/", response_model=MealOut)
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    return crud.create_meal(db, meal)

@router.get("/", response_model=List[MealOut])
def read_all_meals(db: Session = Depends(get_db)):
    return crud.get_all_meals(db)

@router.get("/{meal_id}", response_model=MealOut)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    result = crud.get_meal(db, meal_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return result

@router.put("/{meal_id}", response_model=MealOut)
def update_meal(meal_id: int, meal: MealUpdate, db: Session = Depends(get_db)):
    result = crud.update_meal(db, meal_id, meal)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return result

@router.delete("/{meal_id}", response_model=MealOut)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    result = crud.delete_meal(db, meal_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return result
